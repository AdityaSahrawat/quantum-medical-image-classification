"""
Automated unit and integration test suite for Quantum Medical Image Classification.
"""
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
import tempfile
import numpy as np
import pytest
import torch
import torch.nn as nn
from PIL import Image

from src.data.preprocessing import get_transforms
from src.data.dataset import load_pneumoniamnist, get_dataloaders, WrappedMedMNISTDataset
from src.models.classical_cnn import ClassicalCNN, CNNFeatureExtractor
from src.models.classical_hybrid import ClassicalHybridCNN
from src.models.quantum_circuit import create_quantum_circuit, create_torch_quantum_layer
from src.models.quantum_hybrid import HybridQuantumCNN
from src.evaluation.metrics import compute_classification_metrics, find_optimal_threshold


def test_dataset_loading():
    """Verify official train, val, and test partitions are loaded accurately."""
    train_raw, val_raw, test_raw = load_pneumoniamnist(root="data", download=True)
    assert len(train_raw) == 4708, f"Expected 4708 train samples, got {len(train_raw)}"
    assert len(val_raw) == 524, f"Expected 524 val samples, got {len(val_raw)}"
    assert len(test_raw) == 624, f"Expected 624 test samples, got {len(test_raw)}"
    assert train_raw[0][0].size == (28, 28)


def test_image_and_label_shapes():
    """Verify wrapped dataset yields correct tensor shapes and float data types."""
    train_raw, _, _ = load_pneumoniamnist(root="data", download=True)
    transform = get_transforms(is_train=False)
    wrapped = WrappedMedMNISTDataset(train_raw, transform=transform)

    img, target = wrapped[0]
    assert isinstance(img, torch.Tensor)
    assert img.shape == (1, 28, 28)
    assert img.dtype == torch.float32
    assert img.min() >= 0.0 and img.max() <= 1.0

    assert isinstance(target, torch.Tensor)
    assert target.shape == (1,)
    assert target.item() in (0.0, 1.0)


def test_preprocessing():
    """Verify training augmentation and evaluation transforms."""
    dummy_img = Image.new("L", (28, 28), color=128)

    train_tf = get_transforms(is_train=True)
    eval_tf = get_transforms(is_train=False)

    t_tensor = train_tf(dummy_img)
    e_tensor = eval_tf(dummy_img)

    assert t_tensor.shape == (1, 28, 28)
    assert e_tensor.shape == (1, 28, 28)
    assert 0.0 <= t_tensor.min() and t_tensor.max() <= 1.0
    assert 0.0 <= e_tensor.min() and e_tensor.max() <= 1.0


def test_classical_model_forward():
    """Verify Model A (Classical CNN) forward pass and output shape."""
    model = ClassicalCNN(in_channels=1, conv1_out=16, conv2_out=32, fc_hidden=64)
    x = torch.randn(4, 1, 28, 28)
    out = model(x)
    assert out.shape == (4, 1)


def test_classical_hybrid_forward():
    """Verify Model B (CNN + MLP) forward pass and output shape."""
    model = ClassicalHybridCNN(in_channels=1, conv1_out=16, conv2_out=32, projection_dim=4, mlp_hidden=8)
    x = torch.randn(4, 1, 28, 28)
    out = model(x)
    assert out.shape == (4, 1)


def test_quantum_circuit_forward():
    """Verify 4-qubit variational quantum circuit returns 4 Pauli-Z expectation values."""
    q_layer = create_torch_quantum_layer(n_qubits=4, n_layers=2, rotation="Y")
    inputs = torch.randn(4, 4)
    out = q_layer(inputs)
    assert out.shape == (4, 4)
    # Pauli-Z expectation values must lie in [-1.0, 1.0]
    assert torch.all(out >= -1.0 - 1e-5) and torch.all(out <= 1.0 + 1e-5)


def test_quantum_gradient_computation():
    """Verify analytical gradients flow through quantum circuit weights."""
    q_layer = create_torch_quantum_layer(n_qubits=4, n_layers=2, rotation="Y")
    inputs = torch.randn(2, 4, requires_grad=True)
    out = q_layer(inputs)
    loss = out.sum()
    loss.backward()

    assert inputs.grad is not None
    assert inputs.grad.norm().item() > 0.0
    assert q_layer.weights.grad is not None
    assert q_layer.weights.grad.norm().item() > 0.0


def test_hybrid_quantum_forward_and_backward():
    """Verify Model C (Hybrid Quantum CNN) end-to-end forward pass and backprop."""
    model = HybridQuantumCNN(
        in_channels=1,
        conv1_out=16,
        conv2_out=32,
        n_qubits=4,
        n_layers=2,
        rotation="Y",
    )
    x = torch.randn(4, 1, 28, 28, requires_grad=True)
    logits = model(x)
    assert logits.shape == (4, 1)

    loss = logits.sum()
    loss.backward()

    # Verify gradients reach CNN feature extractor, quantum circuit, and readout classifier
    assert model.feature_extractor.conv_layers[0].weight.grad is not None
    assert model.feature_extractor.conv_layers[0].weight.grad.norm().item() > 0.0
    assert model.quantum_layer.weights.grad is not None
    assert model.quantum_layer.weights.grad.norm().item() > 0.0
    assert model.classifier.weight.grad is not None
    assert model.classifier.weight.grad.norm().item() > 0.0


def test_batch_inference():
    """Verify DataLoader batch evaluation across all models."""
    train_l, val_l, test_l, _ = get_dataloaders(root="data", batch_size=8)
    batch_x, batch_y = next(iter(val_l))

    m_a = ClassicalCNN()
    m_b = ClassicalHybridCNN()
    m_c = HybridQuantumCNN()

    with torch.no_grad():
        out_a = m_a(batch_x)
        out_b = m_b(batch_x)
        out_c = m_c(batch_x)

    assert out_a.shape == (8, 1)
    assert out_b.shape == (8, 1)
    assert out_c.shape == (8, 1)


def test_checkpoint_saving_and_loading():
    """Verify model state saving and recovery preserves parameter values and outputs."""
    model = HybridQuantumCNN(n_layers=2)
    x = torch.randn(2, 1, 28, 28)

    with torch.no_grad():
        initial_out = model(x)

    with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as tmp:
        ckpt_path = tmp.name

    try:
        torch.save({"model_state_dict": model.state_dict()}, ckpt_path)
        new_model = HybridQuantumCNN(n_layers=2)
        new_model.load_state_dict(torch.load(ckpt_path)["model_state_dict"])
        new_model.eval()

        with torch.no_grad():
            loaded_out = new_model(x)

        assert torch.allclose(initial_out, loaded_out, atol=1e-6)
    finally:
        if os.path.exists(ckpt_path):
            os.remove(ckpt_path)


def test_metric_calculation():
    """Verify calculation of accuracy, precision, recall, specificity, f1, and roc_auc."""
    y_true = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.3, 0.8, 0.7, 0.8, 0.9, 0.4])  # 1 FP, 1 FN

    metrics = compute_classification_metrics(y_true, y_prob, threshold=0.5)

    assert metrics["confusion_matrix"]["tn"] == 3
    assert metrics["confusion_matrix"]["fp"] == 1
    assert metrics["confusion_matrix"]["fn"] == 1
    assert metrics["confusion_matrix"]["tp"] == 3

    assert pytest.approx(metrics["accuracy"], 0.01) == 0.75
    assert pytest.approx(metrics["precision"], 0.01) == 0.75
    assert pytest.approx(metrics["recall"], 0.01) == 0.75
    assert pytest.approx(metrics["specificity"], 0.01) == 0.75
    assert pytest.approx(metrics["f1"], 0.01) == 0.75
    assert metrics["roc_auc"] > 0.5
