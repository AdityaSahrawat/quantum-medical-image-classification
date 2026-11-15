"""
Dataset loading and DataLoader construction for PneumoniaMNIST.
"""
import os
from typing import Dict, Optional, Tuple
import medmnist
from medmnist import PneumoniaMNIST
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset, Subset
from sklearn.model_selection import train_test_split

from src.data.preprocessing import get_transforms


class WrappedMedMNISTDataset(Dataset):
    """
    Wrapper around MedMNIST dataset to apply torchvision transforms cleanly
    and yield (image_tensor, label_tensor) where label is a float tensor of shape (1,).
    """
    def __init__(self, medmnist_dataset: Dataset, transform=None):
        self.dataset = medmnist_dataset
        self.transform = transform

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        img, target = self.dataset[idx]
        # img is a PIL Image when no transform is passed to MedMNIST
        if self.transform is not None:
            img = self.transform(img)
        # target in medmnist is a 1D numpy array, e.g. array([1])
        label = torch.tensor(target, dtype=torch.float32)
        return img, label


def load_pneumoniamnist(
    root: str = "data",
    download: bool = True
) -> Tuple[PneumoniaMNIST, PneumoniaMNIST, PneumoniaMNIST]:
    """
    Load raw PneumoniaMNIST datasets for train, val, test splits.
    """
    os.makedirs(root, exist_ok=True)
    train_raw = PneumoniaMNIST(split="train", download=download, root=root)
    val_raw = PneumoniaMNIST(split="val", download=download, root=root)
    test_raw = PneumoniaMNIST(split="test", download=download, root=root)
    return train_raw, val_raw, test_raw


def get_dataset_statistics(train_raw: PneumoniaMNIST, val_raw: PneumoniaMNIST, test_raw: PneumoniaMNIST) -> Dict:
    """
    Inspect and return class distributions, split sizes, and class weights.
    """
    stats = {}
    for split_name, ds in [("train", train_raw), ("val", val_raw), ("test", test_raw)]:
        labels = ds.labels.squeeze()
        n_total = len(labels)
        n_normal = int(np.sum(labels == 0))
        n_pneumonia = int(np.sum(labels == 1))
        stats[split_name] = {
            "total": n_total,
            "normal": n_normal,
            "pneumonia": n_pneumonia,
            "normal_pct": 100.0 * n_normal / n_total,
            "pneumonia_pct": 100.0 * n_pneumonia / n_total,
        }

    # Training class weights for BCEWithLogitsLoss (pos_weight = n_neg / n_pos)
    train_normal = stats["train"]["normal"]
    train_pneumonia = stats["train"]["pneumonia"]
    pos_weight = train_normal / train_pneumonia if train_pneumonia > 0 else 1.0

    stats["pos_weight"] = float(pos_weight)
    stats["class_mapping"] = {0: "Normal", 1: "Pneumonia"}
    return stats


def get_dataloaders(
    root: str = "data",
    batch_size: int = 64,
    subsample_train_size: Optional[int] = None,
    seed: int = 42,
    num_workers: int = 0,
    download: bool = True,
    rotation_degrees: float = 5.0,
    translation: Tuple[float, float] = (0.05, 0.05),
    brightness: float = 0.1,
    contrast: float = 0.1,
) -> Tuple[DataLoader, DataLoader, DataLoader, Dict]:
    """
    Create PyTorch DataLoaders for train, val, test splits.

    Args:
        root: Data directory.
        batch_size: Batch size.
        subsample_train_size: Optional integer to subsample training set reproducibly.
        seed: Random seed for reproducibility.
        num_workers: DataLoader worker count.
        download: Whether to download if absent.
        rotation_degrees: Train augmentation rotation limit.
        translation: Train augmentation translation limit.
        brightness: Train augmentation brightness jitter.
        contrast: Train augmentation contrast jitter.

    Returns:
        (train_loader, val_loader, test_loader, stats_dict)
    """
    train_raw, val_raw, test_raw = load_pneumoniamnist(root=root, download=download)
    stats = get_dataset_statistics(train_raw, val_raw, test_raw)

    train_transform = get_transforms(
        is_train=True,
        rotation_degrees=rotation_degrees,
        translation=translation,
        brightness=brightness,
        contrast=contrast,
    )
    eval_transform = get_transforms(is_train=False)

    train_wrapped = WrappedMedMNISTDataset(train_raw, transform=train_transform)
    val_wrapped = WrappedMedMNISTDataset(val_raw, transform=eval_transform)
    test_wrapped = WrappedMedMNISTDataset(test_raw, transform=eval_transform)

    # Optional reproducible stratified subsampling for training set
    if subsample_train_size is not None and subsample_train_size < len(train_wrapped):
        train_labels = train_raw.labels.squeeze()
        indices = np.arange(len(train_labels))
        sub_indices, _ = train_test_split(
            indices,
            train_size=subsample_train_size,
            stratify=train_labels,
            random_state=seed,
        )
        train_dataset = Subset(train_wrapped, sub_indices)
        stats["train_subsampled_size"] = len(sub_indices)
    else:
        train_dataset = train_wrapped
        stats["train_subsampled_size"] = len(train_wrapped)

    generator = torch.Generator()
    generator.manual_seed(seed)

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        generator=generator,
        pin_memory=False,
    )

    val_loader = DataLoader(
        val_wrapped,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=False,
    )

    test_loader = DataLoader(
        test_wrapped,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=False,
    )

    return train_loader, val_loader, test_loader, stats
