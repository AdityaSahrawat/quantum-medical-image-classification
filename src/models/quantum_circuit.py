"""
Variational Quantum Circuit (VQC) implementation using PennyLane.
"""
from typing import Dict, Optional, Tuple, Any
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
import pennylane as qml
import torch
import torch.nn as nn


def create_quantum_circuit(
    n_qubits: int = 4,
    n_layers: int = 2,
    rotation: str = "Y",
    dev: Optional[Any] = None,
    diff_method: str = "backprop",
):
    """
    Construct the 4-qubit parameterized quantum circuit QNode.

    Specifications:
    - Device: default.qubit (4 wires)
    - Input encoding: AngleEmbedding with rotation='Y'
    - Variational layers: n_layers of single-qubit RX, RY, RZ rotations per qubit
    - Entanglement: Ring of CNOTs: (0,1), (1,2), (2,3), (3,0)
    - Measurement: Pauli-Z expectation values on all 4 qubits
    """
    if dev is None:
        dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev, interface="torch", diff_method=diff_method)
    def qnode(inputs, weights):
        # 1. Angle encoding of 4 classical features
        qml.AngleEmbedding(inputs, wires=range(n_qubits), rotation=rotation)

        # 2. Variational layers: RX, RY, RZ on each qubit + ring entanglement
        for l in range(weights.shape[0]):
            for q in range(n_qubits):
                qml.RX(weights[l, q, 0], wires=q)
                qml.RY(weights[l, q, 1], wires=q)
                qml.RZ(weights[l, q, 2], wires=q)

            # Ring of CNOT gates
            for q in range(n_qubits):
                target_q = (q + 1) % n_qubits
                qml.CNOT(wires=[q, target_q])

        # 3. Measure Pauli-Z expectation values on all qubits
        return [qml.expval(qml.PauliZ(q)) for q in range(n_qubits)]

    return qnode


def create_torch_quantum_layer(
    n_qubits: int = 4,
    n_layers: int = 2,
    rotation: str = "Y",
    dev: Optional[Any] = None,
    diff_method: str = "backprop",
) -> qml.qnn.TorchLayer:
    """
    Construct a differentiable PyTorch layer wrapping the PennyLane QNode.

    Weight shape: (n_layers, n_qubits, 3) for RX, RY, RZ angles.
    """
    circuit = create_quantum_circuit(
        n_qubits=n_qubits,
        n_layers=n_layers,
        rotation=rotation,
        dev=dev,
        diff_method=diff_method,
    )
    weight_shapes = {"weights": (n_layers, n_qubits, 3)}
    torch_layer = qml.qnn.TorchLayer(circuit, weight_shapes)
    return torch_layer
