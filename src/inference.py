"""
Single-image inference script for Classical CNN, Classical Hybrid, and Hybrid Quantum CNN.
"""
import argparse
import os
import sys
# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import yaml
from PIL import Image
import torch
import torchvision.transforms as transforms

from src.models.classical_cnn import ClassicalCNN
from src.models.classical_hybrid import ClassicalHybridCNN
from src.models.quantum_hybrid import HybridQuantumCNN


def load_image(image_path: str) -> torch.Tensor:
    """
    Load an input chest X-ray image, convert to grayscale, resize to 28x28 if needed,
    and convert to normalized float tensor [0, 1] with shape (1, 1, 28, 28).
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    img = Image.open(image_path).convert("L")
    if img.size != (28, 28):
        img = img.resize((28, 28), Image.Resampling.BILINEAR)

    transform = transforms.ToTensor()
    tensor = transform(img).unsqueeze(0)  # Shape: (1, 1, 28, 28)
    return tensor


def run_inference(image_path: str, config_path: str = "configs/config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    device = torch.device(config["project"].get("device", "cpu"))
    ckpt_dir = config["paths"]["checkpoints_dir"]
    in_channels = config["dataset"]["in_channels"]
    class_map = {0: "Normal", 1: "Pneumonia"}

    image_tensor = load_image(image_path).to(device)

    # 1. Classical CNN
    cnn_ckpt = os.path.join(ckpt_dir, "classical_cnn_best.pt")
    cnn_pred_str = "Checkpoint not found"
    cnn_prob_str = "N/A"
    if os.path.exists(cnn_ckpt):
        m_cfg = config["models"]["classical_cnn"]
        model_a = ClassicalCNN(
            in_channels=in_channels,
            conv1_out=m_cfg["conv1_out"],
            conv2_out=m_cfg["conv2_out"],
            fc_hidden=m_cfg["fc_hidden"],
            dropout=m_cfg["dropout"],
        ).to(device)
        model_a.load_state_dict(torch.load(cnn_ckpt, map_location=device)["model_state_dict"])
        model_a.eval()
        with torch.no_grad():
            logit = model_a(image_tensor)
            prob = torch.sigmoid(logit).item()
            pred = 1 if prob >= 0.5 else 0
            cnn_pred_str = class_map[pred]
            cnn_prob_str = f"{prob:.4f}"

    # 2. CNN + MLP
    hybrid_ckpt = os.path.join(ckpt_dir, "cnn_+_mlp_best.pt")
    hybrid_pred_str = "Checkpoint not found"
    hybrid_prob_str = "N/A"
    if os.path.exists(hybrid_ckpt):
        m_cfg = config["models"]["classical_hybrid"]
        model_b = ClassicalHybridCNN(
            in_channels=in_channels,
            conv1_out=m_cfg["conv1_out"],
            conv2_out=m_cfg["conv2_out"],
            projection_dim=m_cfg["projection_dim"],
            mlp_hidden=m_cfg["mlp_hidden"],
            dropout=m_cfg["dropout"],
        ).to(device)
        model_b.load_state_dict(torch.load(hybrid_ckpt, map_location=device)["model_state_dict"])
        model_b.eval()
        with torch.no_grad():
            logit = model_b(image_tensor)
            prob = torch.sigmoid(logit).item()
            pred = 1 if prob >= 0.5 else 0
            hybrid_pred_str = class_map[pred]
            hybrid_prob_str = f"{prob:.4f}"

    # 3. Hybrid Quantum CNN
    qnn_ckpt = os.path.join(ckpt_dir, "hybrid_qnn_best.pt")
    qnn_pred_str = "Checkpoint not found"
    qnn_prob_str = "N/A"
    if os.path.exists(qnn_ckpt):
        m_cfg = config["models"]["quantum_hybrid"]
        model_c = HybridQuantumCNN(
            in_channels=in_channels,
            conv1_out=m_cfg["conv1_out"],
            conv2_out=m_cfg["conv2_out"],
            n_qubits=m_cfg["n_qubits"],
            n_layers=m_cfg["n_layers"],
            rotation=m_cfg["rotation_encoding"],
            diff_method=m_cfg.get("diff_method", "backprop"),
        ).to(device)
        model_c.load_state_dict(torch.load(qnn_ckpt, map_location=device)["model_state_dict"])
        model_c.eval()
        with torch.no_grad():
            logit = model_c(image_tensor)
            prob = torch.sigmoid(logit).item()
            pred = 1 if prob >= 0.5 else 0
            qnn_pred_str = class_map[pred]
            qnn_prob_str = f"{prob:.4f}"

    # Print formatted output matching specification
    print(f"Image: {os.path.basename(image_path)}\n")
    print("Classical CNN:")
    print(f"Prediction: {cnn_pred_str}")
    print(f"Probability: {cnn_prob_str}\n")
    print("CNN + MLP:")
    print(f"Prediction: {hybrid_pred_str}")
    print(f"Probability: {hybrid_prob_str}\n")
    print("Hybrid Quantum CNN:")
    print(f"Prediction: {qnn_pred_str}")
    print(f"Probability: {qnn_prob_str}")

    return {
        "Classical CNN": {"prediction": cnn_pred_str, "probability": cnn_prob_str},
        "CNN + MLP": {"prediction": hybrid_pred_str, "probability": hybrid_prob_str},
        "Hybrid Quantum CNN": {"prediction": qnn_pred_str, "probability": qnn_prob_str},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Inference on Single Chest X-ray Image")
    parser.add_argument("--image", type=str, required=True, help="Path to input chest X-ray image (PNG/JPEG)")
    parser.add_argument("--config", type=str, default="configs/config.yaml", help="Path to config file")
    args = parser.parse_args()
    run_inference(image_path=args.image, config_path=args.config)
