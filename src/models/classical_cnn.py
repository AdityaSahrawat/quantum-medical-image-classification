"""
Classical CNN baseline model and CNN feature extractor for PneumoniaMNIST.
"""
import torch
import torch.nn as nn


class CNNFeatureExtractor(nn.Module):
    """
    Shared CNN feature extractor backbone for hybrid architectures.

    Architecture:
    - Input: 1 x 28 x 28
    - Conv2D: 1 -> conv1_out (default 16), kernel 3, padding 1
    - ReLU
    - MaxPool2D: 2x2 -> (16, 14, 14)
    - Conv2D: conv1_out -> conv2_out (default 32), kernel 3, padding 1
    - ReLU
    - MaxPool2D: 2x2 -> (32, 7, 7)
    - Flatten: conv2_out * 7 * 7 = 1568
    - Projection: Linear(1568, projection_dim)
    """
    def __init__(
        self,
        in_channels: int = 1,
        conv1_out: int = 16,
        conv2_out: int = 32,
        projection_dim: int = 4,
    ):
        super().__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(in_channels, conv1_out, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(conv1_out, conv2_out, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.flatten = nn.Flatten()
        self.flattened_dim = conv2_out * 7 * 7
        self.projection = nn.Linear(self.flattened_dim, projection_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Extract features and project to projection_dim.
        """
        features = self.conv_layers(x)
        flattened = self.flatten(features)
        projected = self.projection(flattened)
        return projected


class ClassicalCNN(nn.Module):
    """
    Model A: Classical CNN Baseline.

    Suggested architecture:
    - Input: 1 x 28 x 28
    - Conv2D: 1 to 16 channels, kernel 3, padding 1
    - ReLU
    - MaxPool2D (2x2)
    - Conv2D: 16 to 32 channels, kernel 3, padding 1
    - ReLU
    - MaxPool2D (2x2)
    - Flatten (1568)
    - Fully connected layer: 64 units
    - ReLU
    - Dropout: 0.3
    - Final output: 1 logit
    """
    def __init__(
        self,
        in_channels: int = 1,
        conv1_out: int = 16,
        conv2_out: int = 32,
        fc_hidden: int = 64,
        dropout: float = 0.3,
    ):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, conv1_out, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv2 = nn.Conv2d(conv1_out, conv2_out, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.flatten = nn.Flatten()
        self.flattened_dim = conv2_out * 7 * 7

        self.fc1 = nn.Linear(self.flattened_dim, fc_hidden)
        self.relu3 = nn.ReLU()
        self.dropout = nn.Dropout(p=dropout)
        self.fc2 = nn.Linear(fc_hidden, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.pool1(self.relu1(self.conv1(x)))
        out = self.pool2(self.relu2(self.conv2(out)))
        out = self.flatten(out)
        out = self.dropout(self.relu3(self.fc1(out)))
        logit = self.fc2(out)
        return logit
