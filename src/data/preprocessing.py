"""
Preprocessing and data augmentation for PneumoniaMNIST images.
"""
from typing import Tuple
from torchvision import transforms


def get_transforms(
    is_train: bool = True,
    rotation_degrees: float = 5.0,
    translation: Tuple[float, float] = (0.05, 0.05),
    brightness: float = 0.1,
    contrast: float = 0.1,
) -> transforms.Compose:
    """
    Construct torchvision transform pipeline for PneumoniaMNIST.

    Specifications:
    1. Grayscale images loaded.
    2. Convert to float tensors in [0, 1].
    3. Retain original 28 x 28 resolution.
    4. Apply mild augmentation ONLY during training (<= 5 deg rotation, minor translation, mild brightness/contrast).
       No vertical flips or aggressive distortions.
    5. Validation and test sets are strictly unaugmented.

    Args:
        is_train: Whether to include mild training augmentation.
        rotation_degrees: Maximum rotation angle in degrees (default 5.0).
        translation: Maximum translation fraction (default (0.05, 0.05)).
        brightness: Brightness jitter factor.
        contrast: Contrast jitter factor.

    Returns:
        torchvision.transforms.Compose pipeline.
    """
    transform_list = []

    if is_train:
        transform_list.extend([
            transforms.RandomAffine(
                degrees=(-rotation_degrees, rotation_degrees),
                translate=translation,
            ),
            transforms.ColorJitter(
                brightness=brightness,
                contrast=contrast,
            ),
        ])

    # Convert PIL Image / ndarray to PyTorch Tensor in range [0.0, 1.0]
    transform_list.append(transforms.ToTensor())

    return transforms.Compose(transform_list)
