"""
Comprehensive evaluation script for all trained models on the held-out PneumoniaMNIST test set.
"""
import argparse
import os
import sys
# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
import time
import yaml
import numpy as np
import torch
from sklearn.metrics import roc_curve, auc

from src.data.dataset import get_dataloaders
from src.models.classical_cnn import ClassicalCNN
from src.models.classical_hybrid import ClassicalHybridCNN
from src.models.quantum_hybrid import HybridQuantumCNN
from src.evaluation.metrics import compute_classification_metrics, find_optimal_threshold
from src.evaluation.visualization import (
    plot_training_curves,
    plot_confusion_matrices,
    plot_combined_roc_curves,
    plot_model_comparison_bar,
    plot_prediction_samples,
    save_quantum_circuit_diagram,
)


def load_model_from_checkpoint(checkpoint_path: str, model_type: str, config: dict):
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found at: {checkpoint_path}")

    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    in_channels = config["dataset"]["in_channels"]

    if model_type == "classical_cnn":
        m_cfg = config["models"]["classical_cnn"]
        model = ClassicalCNN(
            in_channels=in_channels,
            conv1_out=m_cfg["conv1_out"],
            conv2_out=m_cfg["conv2_out"],
            fc_hidden=m_cfg["fc_hidden"],
            dropout=m_cfg["dropout"],
        )
    elif model_type == "classical_hybrid":
        m_cfg = config["models"]["classical_hybrid"]
        model = ClassicalHybridCNN(
            in_channels=in_channels,
            conv1_out=m_cfg["conv1_out"],
            conv2_out=m_cfg["conv2_out"],
            projection_dim=m_cfg["projection_dim"],
            mlp_hidden=m_cfg["mlp_hidden"],
            dropout=m_cfg["dropout"],
        )
    elif model_type in ["quantum_hybrid", "quantum_hybrid_1layer"]:
        m_cfg = config["models"]["quantum_hybrid"]
        n_layers = 1 if model_type == "quantum_hybrid_1layer" else m_cfg.get("n_layers", 2)
        model = HybridQuantumCNN(
            in_channels=in_channels,
            conv1_out=m_cfg["conv1_out"],
            conv2_out=m_cfg["conv2_out"],
            n_qubits=m_cfg["n_qubits"],
            n_layers=n_layers,
            rotation=m_cfg["rotation_encoding"],
            diff_method=m_cfg.get("diff_method", "backprop"),
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model, checkpoint


def evaluate_all(config_path: str = "configs/config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    device = torch.device(config["project"].get("device", "cpu"))
    seed = config["project"]["seed"]

    train_loader, val_loader, test_loader, stats = get_dataloaders(
        root=config["dataset"]["root"],
        batch_size=config["training"]["batch_size"],
        subsample_train_size=config["dataset"].get("subsample_train_size"),
        seed=seed,
    )

    models_info = [
        ("Classical CNN", "classical_cnn", "classical_cnn_best.pt", "classical_cnn_history.json"),
        ("CNN + MLP", "classical_hybrid", "cnn_+_mlp_best.pt", "cnn_+_mlp_history.json"),
        ("Hybrid QNN", "quantum_hybrid", "hybrid_qnn_best.pt", "hybrid_qnn_history.json"),
    ]

    # Check for optional 1-layer ablation checkpoint
    ablation_ckpt = os.path.join(config["paths"]["checkpoints_dir"], "hybrid_qnn_(1-layer)_best.pt")
    if os.path.exists(ablation_ckpt):
        models_info.append(
            ("Hybrid QNN (1-Layer)", "quantum_hybrid_1layer", "hybrid_qnn_(1-layer)_best.pt", "hybrid_qnn_(1-layer)_history.json")
        )

    eval_results = {}
    histories = {}
    roc_data = {}
    confusion_dict = {}

    # Store raw test images for prediction sample plots
    raw_test_images = []
    raw_test_labels = []
    for imgs, lbls in test_loader:
        raw_test_images.append(imgs.numpy())
        raw_test_labels.append(lbls.numpy())
    raw_test_images = np.concatenate(raw_test_images, axis=0)
    raw_test_labels = np.concatenate(raw_test_labels, axis=0).ravel()

    hybrid_preds_for_viz = {}

    for display_name, m_type, ckpt_name, hist_name in models_info:
        ckpt_path = os.path.join(config["paths"]["checkpoints_dir"], ckpt_name)
        hist_path = os.path.join(config["paths"]["metrics_dir"], hist_name)

        if not os.path.exists(ckpt_path):
            print(f"Skipping {display_name}: Checkpoint {ckpt_path} not found.")
            continue

        model, ckpt_data = load_model_from_checkpoint(ckpt_path, m_type, config)
        model.to(device)

        # Load history if available
        training_time = 0.0
        if os.path.exists(hist_path):
            with open(hist_path, "r") as f:
                h_data = json.load(f)
                histories[display_name] = h_data.get("history", {})
                training_time = h_data.get("total_training_time_sec", 0.0)

        # 1. Evaluate on Validation Set to find validation-tuned threshold
        val_probs = []
        val_targets = []
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                logits = model(images)
                probs = torch.sigmoid(logits).cpu().numpy().ravel()
                val_probs.extend(probs)
                val_targets.extend(labels.numpy().ravel())

        val_probs = np.array(val_probs)
        val_targets = np.array(val_targets)
        val_metrics_default = compute_classification_metrics(val_targets, val_probs, threshold=0.5)
        val_opt_threshold, _ = find_optimal_threshold(val_targets, val_probs, criterion="f1")

        # 2. Evaluate on Held-out Test Set (624 images)
        test_probs = []
        test_targets = []
        inference_start = time.time()
        with torch.no_grad():
            for images, labels in test_loader:
                images = images.to(device)
                logits = model(images)
                probs = torch.sigmoid(logits).cpu().numpy().ravel()
                test_probs.extend(probs)
                test_targets.extend(labels.numpy().ravel())
        inference_time = time.time() - inference_start
        per_image_latency_ms = (inference_time / len(test_targets)) * 1000.0

        test_probs = np.array(test_probs)
        test_targets = np.array(test_targets)

        # Default threshold 0.5 metrics
        test_metrics_default = compute_classification_metrics(test_targets, test_probs, threshold=0.5)
        # Validation-tuned threshold metrics
        test_metrics_tuned = compute_classification_metrics(test_targets, test_probs, threshold=val_opt_threshold)

        # ROC Curve data
        fpr, tpr, _ = roc_curve(test_targets, test_probs)
        roc_data[display_name] = (fpr, tpr, test_metrics_default["roc_auc"])
        confusion_dict[display_name] = np.array(test_metrics_default["confusion_matrix"]["matrix"])

        eval_results[display_name] = {
            "test_metrics_default_threshold": test_metrics_default,
            "test_metrics_val_tuned_threshold": test_metrics_tuned,
            "val_metrics_default_threshold": val_metrics_default,
            "val_optimal_threshold": float(val_opt_threshold),
            "training_time_sec": float(training_time),
            "inference_time_sec": float(inference_time),
            "latency_ms_per_image": float(per_image_latency_ms),
            "checkpoint_epoch": ckpt_data.get("epoch"),
        }

        if display_name == "Hybrid QNN":
            hybrid_preds_for_viz["y_true"] = test_targets
            hybrid_preds_for_viz["y_prob"] = test_probs
            hybrid_preds_for_viz["y_pred"] = (test_probs >= 0.5).astype(int)

    # 3. Save Evaluation Results JSON
    metrics_out_path = os.path.join(config["paths"]["metrics_dir"], "test_metrics.json")
    with open(metrics_out_path, "w") as f:
        json.dump(eval_results, f, indent=2)
    print(f"\nSaved test evaluation metrics to {metrics_out_path}")

    # 4. Generate Visualizations
    fig_dir = config["paths"]["figures_dir"]
    os.makedirs(fig_dir, exist_ok=True)

    if histories:
        plot_training_curves(
            histories,
            loss_path=os.path.join(fig_dir, "loss_curves.png"),
            acc_path=os.path.join(fig_dir, "accuracy_curves.png"),
        )
        print("Generated loss and accuracy curves.")

    if confusion_dict:
        plot_confusion_matrices(confusion_dict, save_dir=fig_dir)
        print("Generated confusion matrix heatmaps.")

    if roc_data:
        plot_combined_roc_curves(roc_data, save_path=os.path.join(fig_dir, "roc_curves_combined.png"))
        print("Generated combined ROC curve.")

    # Model comparison bar chart (using default 0.5 threshold)
    summary_for_bar = {
        name: res["test_metrics_default_threshold"]
        for name, res in eval_results.items()
    }
    plot_model_comparison_bar(summary_for_bar, save_path=os.path.join(fig_dir, "model_comparison.png"))
    print("Generated model performance comparison chart.")

    # Correct and incorrect prediction examples
    if "y_true" in hybrid_preds_for_viz:
        plot_prediction_samples(
            raw_test_images,
            hybrid_preds_for_viz["y_true"],
            hybrid_preds_for_viz["y_pred"],
            hybrid_preds_for_viz["y_prob"],
            correct=True,
            save_path=os.path.join(fig_dir, "correct_predictions.png"),
        )
        plot_prediction_samples(
            raw_test_images,
            hybrid_preds_for_viz["y_true"],
            hybrid_preds_for_viz["y_pred"],
            hybrid_preds_for_viz["y_prob"],
            correct=False,
            save_path=os.path.join(fig_dir, "incorrect_predictions.png"),
        )
        print("Generated correct and incorrect prediction example figures.")

    # Quantum Circuit diagram
    save_quantum_circuit_diagram(n_layers=2, save_path=os.path.join(fig_dir, "quantum_circuit_diagram.png"))
    print("Generated quantum circuit diagram.")

    # 5. Print Comparison Table
    print_comparison_table(eval_results)
    return eval_results


def print_comparison_table(results: dict):
    """
    Format and print markdown table as required by Section 9.
    """
    print("\n" + "="*85)
    print("FINAL HELD-OUT TEST EVALUATION COMPARISON (PneumoniaMNIST, N=624)")
    print("="*85)

    headers = ["Metric", "CNN", "CNN + MLP", "Hybrid QNN"]
    # Check if 1-layer ablation is present
    has_ablation = "Hybrid QNN (1-Layer)" in results
    if has_ablation:
        headers.append("Hybrid QNN (1-L)")

    row_keys = [
        ("Accuracy", lambda r: f"{r['test_metrics_default_threshold']['accuracy']*100:.2f}%"),
        ("Precision", lambda r: f"{r['test_metrics_default_threshold']['precision']:.4f}"),
        ("Recall", lambda r: f"{r['test_metrics_default_threshold']['recall']:.4f}"),
        ("Specificity", lambda r: f"{r['test_metrics_default_threshold']['specificity']:.4f}"),
        ("F1", lambda r: f"{r['test_metrics_default_threshold']['f1']:.4f}"),
        ("ROC-AUC", lambda r: f"{r['test_metrics_default_threshold']['roc_auc']:.4f}"),
        ("Training time", lambda r: f"{r['training_time_sec']:.2f}s"),
        ("Inference time", lambda r: f"{r['inference_time_sec']:.2f}s ({r['latency_ms_per_image']:.2f} ms/img)"),
    ]

    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    print(header_line)
    print(sep_line)

    model_keys = ["Classical CNN", "CNN + MLP", "Hybrid QNN"]
    if has_ablation:
        model_keys.append("Hybrid QNN (1-Layer)")

    for label, extractor in row_keys:
        row = [label]
        for m_key in model_keys:
            if m_key in results:
                row.append(extractor(results[m_key]))
            else:
                row.append("N/A")
        print("| " + " | ".join(row) + " |")

    print("\nNote: Inference time is measured on the entire 624-image test set on CPU simulation (PennyLane default.qubit).")
    print("="*85 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate All Models on PneumoniaMNIST Test Set")
    parser.add_argument("--config", type=str, default="configs/config.yaml", help="Path to config file")
    args = parser.parse_args()
    evaluate_all(config_path=args.config)
