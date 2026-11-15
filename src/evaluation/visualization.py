"""
Comprehensive visualization generation for PneumoniaMNIST quantum-classical classification.
"""
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
import math
from typing import Dict, List, Optional, Tuple, Any
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import roc_curve, auc
import pennylane as qml

from src.models.quantum_circuit import create_quantum_circuit


def setup_style():
    """Configure aesthetic, publication-ready style for plots."""
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 13,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 14,
    })


def plot_dataset_samples(
    images: np.ndarray,
    labels: np.ndarray,
    class_mapping: Optional[Dict[int, str]] = None,
    save_path: str = "outputs/figures/dataset_samples.png",
    n_samples_per_class: int = 4,
):
    """
    1. Dataset sample visualization: Grid of Normal vs Pneumonia chest X-rays.
    """
    setup_style()
    if class_mapping is None:
        class_mapping = {0: "Normal", 1: "Pneumonia"}

    labels = labels.squeeze()
    normal_indices = np.where(labels == 0)[0][:n_samples_per_class]
    pneumonia_indices = np.where(labels == 1)[0][:n_samples_per_class]

    fig, axes = plt.subplots(2, n_samples_per_class, figsize=(3 * n_samples_per_class, 6))

    for col_idx, idx in enumerate(normal_indices):
        ax = axes[0, col_idx]
        img = images[idx].squeeze()
        ax.imshow(img, cmap="gray")
        ax.set_title(f"Normal (Idx {idx})")
        ax.axis("off")

    for col_idx, idx in enumerate(pneumonia_indices):
        ax = axes[1, col_idx]
        img = images[idx].squeeze()
        ax.imshow(img, cmap="gray")
        ax.set_title(f"Pneumonia (Idx {idx})")
        ax.axis("off")

    fig.suptitle("PneumoniaMNIST Dataset Samples (28x28 Grayscale)", fontsize=14, y=0.98)
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_class_distribution(
    stats: Dict,
    save_path: str = "outputs/figures/class_distribution.png",
):
    """
    2. Class distribution chart across train, val, and test splits.
    """
    setup_style()
    splits = ["train", "val", "test"]
    split_labels = ["Train (N=4,708)", "Validation (N=524)", "Test (N=624)"]
    normals = [stats[s]["normal"] for s in splits]
    pneumonias = [stats[s]["pneumonia"] for s in splits]

    x = np.arange(len(splits))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    rects1 = ax.bar(x - width/2, normals, width, label="Normal (0)", color="#3498db")
    rects2 = ax.bar(x + width/2, pneumonias, width, label="Pneumonia (1)", color="#e74c3c")

    ax.set_ylabel("Number of Images")
    ax.set_title("PneumoniaMNIST Class Distribution Across Splits")
    ax.set_xticks(x)
    ax.set_xticklabels(split_labels)
    ax.legend()

    # Annotate bars with counts and percentages
    for rects, counts in [(rects1, normals), (rects2, pneumonias)]:
        for i, rect in enumerate(rects):
            h = rect.get_height()
            split_total = stats[splits[i]]["total"]
            pct = 100.0 * h / split_total
            ax.annotate(f"{h}\n({pct:.1f}%)",
                        xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9)

    ax.set_ylim(0, max(pneumonias) * 1.15)
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_training_curves(
    histories: Dict[str, Dict[str, List[float]]],
    loss_path: str = "outputs/figures/loss_curves.png",
    acc_path: str = "outputs/figures/accuracy_curves.png",
):
    """
    3. Training vs validation loss curves.
    4. Accuracy curves.
    """
    setup_style()
    colors = {
        "Classical CNN": "#2980b9",
        "CNN + MLP": "#27ae60",
        "Hybrid QNN": "#8e44ad",
        "Hybrid QNN (1-Layer)": "#d35400",
    }

    # 1. Loss curves
    fig_loss, ax_loss = plt.subplots(figsize=(9, 6))
    for model_name, hist in histories.items():
        epochs = range(1, len(hist["train_loss"]) + 1)
        c = colors.get(model_name, "#333333")
        ax_loss.plot(epochs, hist["train_loss"], label=f"{model_name} (Train)", color=c, linestyle="--", alpha=0.8)
        ax_loss.plot(epochs, hist["val_loss"], label=f"{model_name} (Val)", color=c, linestyle="-", linewidth=2)

    ax_loss.set_title("Training and Validation Loss Across Epochs")
    ax_loss.set_xlabel("Epoch")
    ax_loss.set_ylabel("Loss (BCEWithLogitsLoss)")
    ax_loss.legend(loc="upper right")
    plt.tight_layout()
    os.makedirs(os.path.dirname(loss_path), exist_ok=True)
    plt.savefig(loss_path, dpi=300, bbox_inches="tight")
    plt.close(fig_loss)

    # 2. Accuracy curves
    fig_acc, ax_acc = plt.subplots(figsize=(9, 6))
    for model_name, hist in histories.items():
        epochs = range(1, len(hist["train_acc"]) + 1)
        c = colors.get(model_name, "#333333")
        ax_acc.plot(epochs, hist["train_acc"], label=f"{model_name} (Train)", color=c, linestyle="--", alpha=0.8)
        ax_acc.plot(epochs, hist["val_acc"], label=f"{model_name} (Val)", color=c, linestyle="-", linewidth=2)

    ax_acc.set_title("Training and Validation Accuracy Across Epochs")
    ax_acc.set_xlabel("Epoch")
    ax_acc.set_ylabel("Accuracy")
    ax_acc.set_ylim(0.5, 1.0)
    ax_acc.legend(loc="lower right")
    plt.tight_layout()
    os.makedirs(os.path.dirname(acc_path), exist_ok=True)
    plt.savefig(acc_path, dpi=300, bbox_inches="tight")
    plt.close(fig_acc)


def plot_single_confusion_matrix(
    cm: np.ndarray,
    model_name: str,
    save_path: str,
):
    """
    Plots an individual confusion matrix heatmap.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(6, 5))
    class_names = ["Normal (0)", "Pneumonia (1)"]

    # Compute percentages normalized over true labels
    cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)

    annot = np.empty_like(cm).astype(str)
    for i in range(2):
        for j in range(2):
            annot[i, j] = f"{cm[i, j]}\n({cm_norm[i, j]*100:.1f}%)"

    sns.heatmap(cm, annot=annot, fmt="", cmap="Blues", cbar=True,
                xticklabels=class_names, yticklabels=class_names, ax=ax)

    ax.set_title(f"Confusion Matrix: {model_name}\n(Test Set, N={cm.sum()})")
    ax.set_ylabel("True Diagnosis")
    ax.set_xlabel("Predicted Diagnosis")
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_confusion_matrices(
    confusion_dict: Dict[str, np.ndarray],
    save_dir: str = "outputs/figures",
):
    """
    5, 6, 7. Generate confusion matrix heatmaps for CNN, CNN+MLP, and Hybrid QNN.
    """
    filename_map = {
        "Classical CNN": "confusion_matrix_cnn.png",
        "CNN + MLP": "confusion_matrix_classical_hybrid.png",
        "Hybrid QNN": "confusion_matrix_quantum_hybrid.png",
    }
    for model_name, cm in confusion_dict.items():
        fname = filename_map.get(model_name, f"confusion_matrix_{model_name.lower().replace(' ', '_')}.png")
        save_path = os.path.join(save_dir, fname)
        plot_single_confusion_matrix(np.array(cm), model_name, save_path)


def plot_combined_roc_curves(
    roc_data: Dict[str, Tuple[np.ndarray, np.ndarray, float]],
    save_path: str = "outputs/figures/roc_curves_combined.png",
):
    """
    8. Combined ROC curve for all models on held-out test set.
    roc_data: Dict mapping model_name -> (fpr, tpr, roc_auc)
    """
    setup_style()
    colors = {
        "Classical CNN": "#2980b9",
        "CNN + MLP": "#27ae60",
        "Hybrid QNN": "#8e44ad",
        "Hybrid QNN (1-Layer)": "#d35400",
    }

    fig, ax = plt.subplots(figsize=(7, 6))
    for model_name, (fpr, tpr, roc_auc) in roc_data.items():
        c = colors.get(model_name, "#333333")
        ax.plot(fpr, tpr, color=c, lw=2.2, label=f"{model_name} (AUC = {roc_auc:.4f})")

    ax.plot([0, 1], [0, 1], color="navy", lw=1.5, linestyle="--", label="Chance (AUC = 0.5000)")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate (1 - Specificity)")
    ax.set_ylabel("True Positive Rate (Sensitivity / Recall)")
    ax.set_title("Receiver Operating Characteristic (ROC) Comparison\n(Held-out Test Set, N=624)")
    ax.legend(loc="lower right")
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_model_comparison_bar(
    metrics_summary: Dict[str, Dict[str, float]],
    save_path: str = "outputs/figures/model_comparison.png",
):
    """
    9. Model performance comparison chart (grouped bar chart).
    """
    setup_style()
    metric_keys = ["accuracy", "precision", "recall", "specificity", "f1", "roc_auc"]
    metric_names = ["Accuracy", "Precision", "Recall", "Specificity", "F1-Score", "ROC-AUC"]

    models = list(metrics_summary.keys())
    x = np.arange(len(metric_keys))
    width = 0.8 / len(models)

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#2980b9", "#27ae60", "#8e44ad", "#d35400"]

    for i, model_name in enumerate(models):
        values = [metrics_summary[model_name].get(k, 0.0) for k in metric_keys]
        offset = (i - len(models)/2 + 0.5) * width
        rects = ax.bar(x + offset, values, width, label=model_name, color=colors[i % len(colors)])

        for rect in rects:
            h = rect.get_height()
            ax.annotate(f"{h:.3f}",
                        xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 2),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, rotation=90)

    ax.set_ylabel("Score")
    ax.set_title("Performance Metrics Comparison Across Models (Test Set)")
    ax.set_xticks(x)
    ax.set_xticklabels(metric_names)
    ax.set_ylim(0.0, 1.15)
    ax.legend(loc="upper left")
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_quantum_circuit_diagram(
    n_layers: int = 2,
    save_path: str = "outputs/figures/quantum_circuit_diagram.png",
):
    """
    10. Quantum circuit diagram.
    Uses PennyLane's matplotlib drawer to render the exact circuit architecture.
    """
    setup_style()
    dev = qml.device("default.qubit", wires=4)
    circuit = create_quantum_circuit(n_qubits=4, n_layers=n_layers, rotation="Y", dev=dev)

    dummy_inputs = np.array([0.5, -0.2, 0.8, -0.4])
    dummy_weights = np.zeros((n_layers, 4, 3))

    fig, ax = qml.draw_mpl(circuit, decimals=2)(dummy_inputs, dummy_weights)
    fig.suptitle(f"Variational Quantum Circuit Architecture ({n_layers} Layers, 4 Qubits)", fontsize=14, y=0.95)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_prediction_samples(
    images: np.ndarray,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
    correct: bool = True,
    class_mapping: Optional[Dict[int, str]] = None,
    save_path: str = "outputs/figures/correct_predictions.png",
    n_samples: int = 8,
):
    """
    11, 12. Correct and incorrect prediction examples.
    """
    setup_style()
    if class_mapping is None:
        class_mapping = {0: "Normal", 1: "Pneumonia"}

    y_true = np.asarray(y_true).squeeze()
    y_pred = np.asarray(y_pred).squeeze()
    y_prob = np.asarray(y_prob).squeeze()

    match_mask = (y_true == y_pred) if correct else (y_true != y_pred)
    candidate_indices = np.where(match_mask)[0]

    if len(candidate_indices) == 0:
        return

    selected_indices = candidate_indices[:n_samples]
    cols = 4
    rows = math.ceil(len(selected_indices) / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(3.5 * cols, 3.5 * rows))
    axes = np.array(axes).reshape(-1)

    for i, idx in enumerate(selected_indices):
        ax = axes[i]
        img = images[idx].squeeze()
        true_name = class_mapping.get(int(y_true[idx]), str(y_true[idx]))
        pred_name = class_mapping.get(int(y_pred[idx]), str(y_pred[idx]))
        prob = y_prob[idx]

        ax.imshow(img, cmap="gray")
        color = "green" if correct else "red"
        ax.set_title(
            f"True: {true_name}\nPred: {pred_name} (p={prob:.3f})",
            color=color,
            fontsize=10,
        )
        ax.axis("off")

    for j in range(len(selected_indices), len(axes)):
        axes[j].axis("off")

    status_str = "Correct Predictions" if correct else "Incorrect Predictions / Error Analysis"
    fig.suptitle(f"Hybrid Quantum-Classical Model: {status_str}", fontsize=13, y=0.98)
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
