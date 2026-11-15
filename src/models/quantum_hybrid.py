"""
Model C: Hybrid Quantum-Classical Convolutional Neural Network.
"""
import math
import torch
import torch.nn as nn
from src.models.classical_cnn import CNNFeatureExtractor
from src.models.quantum_circuit import create_torch_quantum_layer


class HybridQuantumCNN(nn.Module):
    """
    Model C: Hybrid Quantum-Classical CNN.

    Pipeline:
    1. Input image: 1 x 28 x 28
    2. Classical CNN feature extractor (Conv1 -> ReLU -> Pool -> Conv2 -> ReLU -> Pool -> Flatten)
    3. Classical projection to 4 features
    4. Scaling features to [-pi, pi] for angle embedding
    5. Four-qubit variational quantum circuit (AngleEmbedding + RX/RY/RZ + Ring CNOTs)
    6. Four Pauli-Z expectation values
    7. Classical linear output layer: Linear(4, 1)
    8. Binary classification logit
    """
    def __init__(
        self,
        in_channels: int = 1,
        conv1_out: int = 16,
        conv2_out: int = 32,
        n_qubits: int = 4,
        n_layers: int = 2,
        rotation: str = "Y",
        diff_method: str = "backprop",
    ):
        super().__init__()
        self.n_qubits = n_qubits
        self.n_layers = n_layers

        # 1-3. Shared CNN feature extractor projecting to 4 dimensions
        self.feature_extractor = CNNFeatureExtractor(
            in_channels=in_channels,
            conv1_out=conv1_out,
            conv2_out=conv2_out,
            projection_dim=n_qubits,
        )

        # 4-6. Quantum variational circuit layer
        self.quantum_layer = create_torch_quantum_layer(
            n_qubits=n_qubits,
            n_layers=n_layers,
            rotation=rotation,
            diff_method=diff_method,
        )

        # 7-8. Trainable classical linear layer to produce 1 binary logit
        self.classifier = nn.Linear(n_qubits, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through CNN -> feature scaling -> VQC -> Linear classifier.
        """
        # Feature extraction: (B, 1, 28, 28) -> (B, 4)
        features = self.feature_extractor(x)

        # Scale features smoothly into [-pi, pi] for angle embedding
        scaled_angles = torch.tanh(features) * math.pi

        # Quantum layer: (B, 4) -> (B, 4) Pauli-Z expectation values in [-1, 1]
        quantum_expvals = self.quantum_layer(scaled_angles)

        # Classical readout: (B, 4) -> (B, 1) logit
        logit = self.classifier(quantum_expvals)
        return logit

    def extract_latent_and_quantum_features(self, x: torch.Tensor):
        """
        Helper method to inspect intermediate representations (4D classical features and 4D quantum expectations).
        """
        features = self.feature_extractor(x)
        scaled_angles = torch.tanh(features) * math.pi
        quantum_expvals = self.quantum_layer(scaled_angles)
        return features, quantum_expvals
