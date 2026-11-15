"""
Training script for Hybrid Quantum-Classical CNN (Model C and Ablation).
"""
import argparse
import os
import sys
# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import yaml
import torch

from src.data.dataset import get_dataloaders
from src.models.quantum_hybrid import HybridQuantumCNN
from src.training.trainer import Trainer, set_seed


def train_quantum(
    config_path: str = "configs/config.yaml",
    n_layers: int = 2,
    run_ablation: bool = False,
):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    seed = config["project"]["seed"]
    set_seed(seed)
    device = config["project"]["device"]

    # 1. Load Data
    train_loader, val_loader, test_loader, stats = get_dataloaders(
        root=config["dataset"]["root"],
        batch_size=config["training"]["batch_size"],
        subsample_train_size=config["dataset"].get("subsample_train_size"),
        seed=seed,
        num_workers=config["training"].get("num_workers", 0),
        rotation_degrees=config["preprocessing"]["augmentation"]["rotation_degrees"],
        translation=tuple(config["preprocessing"]["augmentation"]["translation"]),
        brightness=config["preprocessing"]["augmentation"]["brightness"],
        contrast=config["preprocessing"]["augmentation"]["contrast"],
    )

    pos_weight = stats["pos_weight"] if config["training"]["loss"].get("use_pos_weight", True) else None

    # Determine layers to train
    layer_configs = [n_layers]
    if run_ablation:
        layer_configs = [1, 2]

    for layers in layer_configs:
        model_name = "Hybrid QNN" if layers == 2 else "Hybrid QNN (1-Layer)"
        checkpoint_name = "hybrid_qnn" if layers == 2 else "hybrid_qnn_1layer"

        print(f"\n==========================================")
        print(f"Preparing {model_name} ({layers} Variational Layers, 4 Qubits)")
        print(f"==========================================")

        m_cfg = config["models"]["quantum_hybrid"]
        model = HybridQuantumCNN(
            in_channels=config["dataset"]["in_channels"],
            conv1_out=m_cfg["conv1_out"],
            conv2_out=m_cfg["conv2_out"],
            n_qubits=m_cfg["n_qubits"],
            n_layers=layers,
            rotation=m_cfg["rotation_encoding"],
            diff_method=m_cfg.get("diff_method", "backprop"),
        )

        trainer = Trainer(
            model=model,
            model_name=model_name,
            train_loader=train_loader,
            val_loader=val_loader,
            device=device,
            lr=config["training"]["optimizer"]["lr"],
            weight_decay=config["training"]["optimizer"]["weight_decay"],
            epochs=config["training"]["epochs"],
            early_stopping_patience=config["training"]["early_stopping"]["patience"],
            pos_weight=pos_weight,
            checkpoint_dir=config["paths"]["checkpoints_dir"],
            metrics_dir=config["paths"]["metrics_dir"],
            config=config,
        )
        trainer.train()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Hybrid Quantum-Classical PneumoniaMNIST Model")
    parser.add_argument("--config", type=str, default="configs/config.yaml", help="Path to config file")
    parser.add_argument("--layers", type=int, default=2, help="Number of variational layers (default: 2)")
    parser.add_argument("--ablation", action="store_true", help="Run ablation (train both 1-layer and 2-layer)")
    args = parser.parse_args()
    train_quantum(config_path=args.config, n_layers=args.layers, run_ablation=args.ablation)
