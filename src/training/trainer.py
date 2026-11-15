"""
Modular trainer for Classical and Quantum-Classical models.
"""
import os
import json
import time
from typing import Dict, Optional, Tuple, Any
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from src.evaluation.metrics import compute_classification_metrics


def set_seed(seed: int = 42):
    """Set random seeds for complete reproducibility across libraries."""
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


class Trainer:
    """
    Standardized Trainer for all three model architectures:
    1. Classical CNN
    2. Classical Hybrid (CNN + MLP)
    3. Quantum Hybrid (CNN + 4-qubit VQC)
    """
    def __init__(
        self,
        model: nn.Module,
        model_name: str,
        train_loader: DataLoader,
        val_loader: DataLoader,
        device: str = "cpu",
        lr: float = 0.001,
        weight_decay: float = 0.0001,
        epochs: int = 25,
        early_stopping_patience: int = 5,
        early_stopping_min_delta: float = 0.001,
        pos_weight: Optional[float] = None,
        checkpoint_dir: str = "outputs/checkpoints",
        metrics_dir: str = "outputs/metrics",
        tb_log_dir: Optional[str] = "runs",
        config: Optional[Dict[str, Any]] = None,
    ):
        self.model = model.to(device)
        self.model_name = model_name
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = torch.device(device)
        self.epochs = epochs
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_min_delta = early_stopping_min_delta
        self.checkpoint_dir = checkpoint_dir
        self.metrics_dir = metrics_dir
        self.config = config or {}

        os.makedirs(checkpoint_dir, exist_ok=True)
        os.makedirs(metrics_dir, exist_ok=True)

        # Loss function with optional pos_weight for class imbalance
        if pos_weight is not None:
            pw_tensor = torch.tensor([pos_weight], dtype=torch.float32, device=self.device)
            self.criterion = nn.BCEWithLogitsLoss(pos_weight=pw_tensor)
        else:
            self.criterion = nn.BCEWithLogitsLoss()

        # Optimizer & Scheduler
        self.optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=lr,
            weight_decay=weight_decay,
        )
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode="min",
            factor=0.5,
            patience=2,
            min_lr=1e-5,
        )

        # TensorBoard writer
        if tb_log_dir:
            run_path = os.path.join(tb_log_dir, model_name)
            os.makedirs(run_path, exist_ok=True)
            self.writer = SummaryWriter(log_dir=run_path)
        else:
            self.writer = None

        self.history = {
            "epoch": [],
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": [],
            "val_f1": [],
            "learning_rate": [],
            "epoch_duration_sec": [],
        }

    def train_epoch(self) -> Tuple[float, float]:
        """Run single training epoch."""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in self.train_loader:
            images = images.to(self.device)
            labels = labels.to(self.device)

            self.optimizer.zero_grad()
            logits = self.model(images)
            loss = self.criterion(logits, labels)
            loss.backward()
            self.optimizer.step()

            running_loss += loss.item() * images.size(0)
            preds = (torch.sigmoid(logits) >= 0.5).float()
            correct += (preds == labels).sum().item()
            total += images.size(0)

        epoch_loss = running_loss / total if total > 0 else 0.0
        epoch_acc = correct / total if total > 0 else 0.0
        return epoch_loss, epoch_acc

    @torch.no_grad()
    def evaluate_loader(self, loader: DataLoader, threshold: float = 0.5) -> Tuple[float, Dict, np.ndarray, np.ndarray]:
        """
        Evaluate on any given DataLoader.
        Returns: (mean_loss, metrics_dict, y_true_arr, y_prob_arr)
        """
        self.model.eval()
        running_loss = 0.0
        total = 0
        all_labels = []
        all_probs = []

        for images, labels in loader:
            images = images.to(self.device)
            labels = labels.to(self.device)

            logits = self.model(images)
            loss = self.criterion(logits, labels)

            running_loss += loss.item() * images.size(0)
            total += images.size(0)

            probs = torch.sigmoid(logits).cpu().numpy().ravel()
            all_probs.extend(probs)
            all_labels.extend(labels.cpu().numpy().ravel())

        mean_loss = running_loss / total if total > 0 else 0.0
        y_true = np.array(all_labels)
        y_prob = np.array(all_probs)
        metrics = compute_classification_metrics(y_true, y_prob, threshold=threshold)
        return mean_loss, metrics, y_true, y_prob

    def train(self) -> Dict[str, Any]:
        """
        Execute full training loop with early stopping, scheduler, checkpointing, and logging.
        """
        best_val_loss = float("inf")
        best_epoch = 0
        epochs_no_improve = 0
        total_start_time = time.time()
        best_checkpoint_path = os.path.join(self.checkpoint_dir, f"{self.model_name.lower().replace(' ', '_')}_best.pt")

        print(f"\n==========================================")
        print(f"Starting Training: {self.model_name}")
        print(f"Epochs: {self.epochs} | Device: {self.device} | Early Stop Patience: {self.early_stopping_patience}")
        print(f"==========================================")

        for epoch in range(1, self.epochs + 1):
            epoch_start = time.time()

            train_loss, train_acc = self.train_epoch()
            val_loss, val_metrics, _, _ = self.evaluate_loader(self.val_loader)
            epoch_duration = time.time() - epoch_start
            current_lr = self.optimizer.param_groups[0]["lr"]

            # Step LR scheduler based on validation loss
            self.scheduler.step(val_loss)

            # Record metrics
            self.history["epoch"].append(epoch)
            self.history["train_loss"].append(float(train_loss))
            self.history["train_acc"].append(float(train_acc))
            self.history["val_loss"].append(float(val_loss))
            self.history["val_acc"].append(float(val_metrics["accuracy"]))
            self.history["val_f1"].append(float(val_metrics["f1"]))
            self.history["learning_rate"].append(float(current_lr))
            self.history["epoch_duration_sec"].append(float(epoch_duration))

            # Tensorboard
            if self.writer:
                self.writer.add_scalar("Loss/Train", train_loss, epoch)
                self.writer.add_scalar("Loss/Val", val_loss, epoch)
                self.writer.add_scalar("Accuracy/Train", train_acc, epoch)
                self.writer.add_scalar("Accuracy/Val", val_metrics["accuracy"], epoch)
                self.writer.add_scalar("F1/Val", val_metrics["f1"], epoch)
                self.writer.add_scalar("LR", current_lr, epoch)

            print(f"Epoch {epoch:02d}/{self.epochs:02d} | "
                  f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc*100:.2f}% | "
                  f"Val Loss: {val_loss:.4f} | Val Acc: {val_metrics['accuracy']*100:.2f}% | "
                  f"Val F1: {val_metrics['f1']:.4f} | LR: {current_lr:.6f} | "
                  f"Time: {epoch_duration:.2f}s")

            # Checkpoint and Early Stopping Check
            if val_loss < (best_val_loss - self.early_stopping_min_delta):
                best_val_loss = val_loss
                best_epoch = epoch
                epochs_no_improve = 0

                checkpoint_data = {
                    "epoch": epoch,
                    "model_name": self.model_name,
                    "model_state_dict": self.model.state_dict(),
                    "optimizer_state_dict": self.optimizer.state_dict(),
                    "val_loss": val_loss,
                    "val_metrics": val_metrics,
                    "config": self.config,
                }
                torch.save(checkpoint_data, best_checkpoint_path)
                print(f"  --> Best model saved (Epoch {epoch}, Val Loss: {val_loss:.4f})")
            else:
                epochs_no_improve += 1
                if epochs_no_improve >= self.early_stopping_patience:
                    print(f"\nEarly stopping triggered after {epoch} epochs (no improvement for {self.early_stopping_patience} epochs).")
                    break

        total_training_time = time.time() - total_start_time
        print(f"Training completed in {total_training_time:.2f}s | Best Val Loss: {best_val_loss:.4f} (Epoch {best_epoch})\n")

        if self.writer:
            self.writer.close()

        # Save history json
        history_path = os.path.join(self.metrics_dir, f"{self.model_name.lower().replace(' ', '_')}_history.json")
        save_data = {
            "model_name": self.model_name,
            "best_epoch": best_epoch,
            "best_val_loss": float(best_val_loss),
            "total_training_time_sec": float(total_training_time),
            "history": self.history,
            "config": self.config,
        }
        with open(history_path, "w") as f:
            json.dump(save_data, f, indent=2)

        return save_data
