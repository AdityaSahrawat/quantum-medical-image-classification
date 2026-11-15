"""
Model B: CNN + Classical MLP (Classical Hybrid Control Model).
"""
import torch
import torch.nn as nn
from src.models.classical_cnn import CNNFeatureExtractor


class ClassicalHybridCNN(nn.Module):
    """
    Model B: Classical Control Model.

    Architecture:
    - Same CNN feature extractor used by the quantum model.
    - Classical feature projection to 4 dimensions.
    - Small trainable MLP (e.g., 4 -> hidden -> 1 logit, matching the capacity of the variational quantum circuit).
    - Binary classification logit.
    """
    def __init__(
        self,
        in_channels: int = 1,
        conv1_out: int = 16,
        conv2_out: int = 32,
        projection_dim: int = 4,
        mlp_hidden: int = 8,
        dropout: float = 0.2,
    ):
        super().__init__()
        self.feature_extractor = CNNFeatureExtractor(
            in_channels=in_channels,
            conv1_out=conv1_out,
            conv2_out=conv2_out,
            projection_dim=projection_dim,
        )
        self.mlp = nn.Sequential(
            nn.Linear(projection_dim, mlp_hidden),
            nn.ReLU(),
            nn.Dropout(p=dropout),
            nn.Linear(mlp_hidden, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass:
        Image (B, 1, 28, 28) -> Features (B, 4) -> MLP -> Logit (B, 1)
        """
        features_4d = self.feature_extractor(x)
        logit = self.mlp(features_4d)
        return logit

    def extract_4d_features(self, x: torch.Tensor) -> torch.Tensor:
        """
        Helper method to extract the intermediate 4-dimensional representation.
        """
        return self.feature_extractor(x)
