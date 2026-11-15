"""
Training script for classical models (Model A: Classical CNN and Model B: CNN + MLP).
"""
import argparse
import os
import sys
# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import yaml
import torch

from src.data.dataset import get_dataloaders
from src.models.classical_cnn import ClassicalCNN
from src.models.classical_hybrid import ClassicalHybridCNN
from src.training.trainer import Trainer, set_seed


def train_classical(config_path: str = "configs/config.yaml", target_model: str = "all"):
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

    # Train Model A: Classical CNN
    if target_model in ["all", "cnn", "classical_cnn"]:
        m_cfg = config["models"]["classical_cnn"]
        model_a = ClassicalCNN(
            in_channels=config["dataset"]["in_channels"],
            conv1_out=m_cfg["conv1_out"],
            conv2_out=m_cfg["conv2_out"],
            fc_hidden=m_cfg["fc_hidden"],
            dropout=m_cfg["dropout"],
        )
        trainer_a = Trainer(
            model=model_a,
            model_name="Classical CNN",
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
        trainer_a.train()

    # Train Model B: Classical Hybrid (CNN + MLP)
    if target_model in ["all", "hybrid", "classical_hybrid"]:
        m_cfg = config["models"]["classical_hybrid"]
        model_b = ClassicalHybridCNN(
            in_channels=config["dataset"]["in_channels"],
            conv1_out=m_cfg["conv1_out"],
            conv2_out=m_cfg["conv2_out"],
            projection_dim=m_cfg["projection_dim"],
            mlp_hidden=m_cfg["mlp_hidden"],
            dropout=m_cfg["dropout"],
        )
        trainer_b = Trainer(
            model=model_b,
            model_name="CNN + MLP",
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
        trainer_b.train()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Classical PneumoniaMNIST Models")
    parser.add_argument("--config", type=str, default="configs/config.yaml", help="Path to config file")
    parser.add_argument("--model", type=str, default="all", choices=["all", "cnn", "classical_hybrid"], help="Target model to train")
    args = parser.parse_args()
    train_classical(config_path=args.config, target_model=args.model)
