# Quantum Medical Image Classification: Hybrid Quantum-Classical Deep Learning on PneumoniaMNIST

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2+-ee4c2c.svg)](https://pytorch.org/)
[![PennyLane](https://img.shields.io/badge/PennyLane-0.36+-brightgreen.svg)](https://pennylane.ai/)
[![MedMNIST](https://img.shields.io/badge/MedMNIST-3.0+-orange.svg)](https://medmnist.com/)
[![Tests](https://img.shields.io/badge/tests-11%2F11%20passing-brightgreen.svg)]()

Academic semester research project investigating whether a variational quantum circuit (VQC) integrated with a classical convolutional neural network (CNN) feature extractor provides competitive classification performance compared to conventional classical architectures for chest radiograph classification.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Medical Motivation](#3-medical-motivation)
4. [Dataset Description](#4-dataset-description)
5. [Dataset Preprocessing & Augmentation](#5-dataset-preprocessing--augmentation)
6. [Classical CNN Architecture (Model A)](#6-classical-cnn-architecture-model-a)
7. [Hybrid Quantum-Classical Architecture (Model C) & Control (Model B)](#7-hybrid-quantum-classical-architecture-model-c--control-model-b)
8. [Quantum Feature Encoding](#8-quantum-feature-encoding)
9. [Variational Quantum Circuit](#9-variational-quantum-circuit)
10. [Entanglement Topology](#10-entanglement-topology)
11. [Quantum Measurement & Readout](#11-quantum-measurement--readout)
12. [Training Methodology & Imbalance Mitigation](#12-training-methodology--imbalance-mitigation)
13. [Evaluation Metrics](#13-evaluation-metrics)
14. [Experimental Results & Comparison](#14-experimental-results--comparison)
15. [Ablation Experiments](#15-ablation-experiments)
16. [Limitations & Ethical Considerations](#16-limitations--ethical-considerations)
17. [Reproducibility Instructions](#17-reproducibility-instructions)
18. [References](#18-references)

---

## 1. Project Overview

This project presents a rigorous end-to-end investigation into hybrid quantum-classical neural networks (HQNN) applied to pediatric chest X-ray diagnosis. We implement, train, and benchmark three controlled model architectures on the standardized **PneumoniaMNIST** benchmark from MedMNIST v2:

- **Model A (Classical CNN Baseline)**: Standard 2-stage convolutional network with dense classification head (105,281 parameters).
- **Model B (CNN + Classical MLP Control)**: The identical CNN backbone projecting down to 4 latent dimensions, followed by a lightweight classical multilayer perceptron (11,125 parameters).
- **Model C (Hybrid Quantum CNN)**: The identical CNN backbone projecting down to 4 latent dimensions, feeding into a 4-qubit parameterized variational quantum circuit (VQC) with ring entanglement and Pauli-$Z$ expectation measurements, decoded by a single linear readout layer (11,105 parameters).

All models are trained with identical data splits, random seeds ($42$), and training configurations, and evaluated against the official held-out test set ($N=624$).

---

## 2. Problem Statement

Binary medical image classification: Given a single-channel grayscale chest radiograph $X \in \mathbb{R}^{1 \times 28 \times 28}$, predict the diagnostic diagnosis $y \in \{0, 1\}$, where:
- $y = 0$: **Normal** (no pulmonary infiltrates).
- $y = 1$: **Pneumonia** (presence of bacterial or viral consolidation).

### Primary Research Question
*Can a variational quantum circuit integrated with a classical CNN feature extractor provide competitive classification performance compared with conventional classical neural networks on low-resolution medical imaging benchmarks?*

---

## 3. Medical Motivation

Pneumonia remains one of the leading infectious causes of pediatric mortality worldwide, accounting for over 700,000 deaths annually among children under five. Early and accurate detection on chest radiographs (CXRs) is essential for timely administration of antibiotics or supportive therapy. 

While classical deep learning models demonstrate strong diagnostic capabilities, they typically require large parameter budgets. Variational Quantum Circuits offer a fundamentally different computational paradigm: by exploiting high-dimensional Hilbert spaces, quantum state superposition, and entanglement, VQCs can represent complex non-linear decision boundaries with very few classical variational parameters. This study evaluates whether this theoretical parameter efficiency translates to empirical medical classification benchmarks without clinical or computational overclaims.

---

## 4. Dataset Description

We utilize the official **PneumoniaMNIST** dataset from the MedMNIST v2 benchmark suite (derived from the Kermany et al. cohort):

- **Total Images**: 5,856
- **Spatial Dimensions**: $28 \times 28$ pixels
- **Channels**: 1 (Grayscale)
- **Official Partitions**:

| Partition | Normal ($0$) | Pneumonia ($1$) | Total | Normal % | Pneumonia % |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Train** | 1,214 | 3,494 | **4,708** | 25.79% | 74.21% |
| **Validation** | 135 | 389 | **524** | 25.76% | 74.24% |
| **Test** | 234 | 390 | **624** | 37.50% | 62.50% |
| **Combined** | 1,583 | 4,273 | **5,856** | 27.03% | 72.97% |

The dataset exhibits notable class imbalance: Pneumonia cases comprise ~74.2% of the training and validation sets and 62.5% of the held-out test set. We preserve the official partitions strictly and do not combine or randomly repartition the data.

---

## 5. Dataset Preprocessing & Augmentation

The preprocessing pipeline enforces deterministic, standardized behavior across all models:
1. **Grayscale Loading**: Raw radiographs loaded as single-channel $28 \times 28$ arrays.
2. **Dynamic Range Scaling**: Transformed via `transforms.ToTensor()` to float tensors in $[0.0, 1.0]$.
3. **Training Augmentation**: Mild transformations applied **only** to the training split:
   - Small rotations: $\pm 5^\circ$ (`transforms.RandomAffine(degrees=(-5, 5))`)
   - Small translations: $\le 5\%$ along both axes (`translate=(0.05, 0.05)`)
   - Mild photometric jitter: Brightness and contrast factor $\pm 0.1$ (`transforms.ColorJitter(brightness=0.1, contrast=0.1)`)
   - *No vertical flips* or aggressive shear transforms that violate radiograph anatomies.
4. **Validation & Test Sets**: Strictly unaugmented; converted purely to $[0.0, 1.0]$ tensors.

---

## 6. Classical CNN Architecture (Model A)

Model A serves as the conventional deep learning baseline:
- **Input**: $(B, 1, 28, 28)$
- **Conv Layer 1**: $\text{Conv2D}(1 \to 16, \text{kernel}=3, \text{pad}=1) \to \text{ReLU} \to \text{MaxPool2D}(2, 2)$ $\implies (B, 16, 14, 14)$
- **Conv Layer 2**: $\text{Conv2D}(16 \to 32, \text{kernel}=3, \text{pad}=1) \to \text{ReLU} \to \text{MaxPool2D}(2, 2)$ $\implies (B, 32, 7, 7)$
- **Flatten**: $32 \times 7 \times 7 = 1,568$ units
- **Dense Layer 1**: $\text{Linear}(1568 \to 64) \to \text{ReLU} \to \text{Dropout}(p=0.3)$
- **Output Layer**: $\text{Linear}(64 \to 1)$ logit
- **Total Parameters**: 105,281

---

## 7. Hybrid Quantum-Classical Architecture (Model C) & Control (Model B)

To isolate the contribution of the quantum circuit from architectural bias, Models B and C share the **exact same CNN feature extractor backbone**:
- $\text{Conv2D}(1 \to 16) \to \text{ReLU} \to \text{MaxPool2D}(2, 2)$
- $\text{Conv2D}(16 \to 32) \to \text{ReLU} \to \text{MaxPool2D}(2, 2)$
- $\text{Flatten} \to \text{Linear}(1568 \to 4)$ latent features

### Model B: CNN + Classical MLP (Control)
- Input: 4 classical latent features
- Trainable MLP: $\text{Linear}(4 \to 8) \to \text{ReLU} \to \text{Dropout}(p=0.2) \to \text{Linear}(8 \to 1)$
- **Total Parameters**: 11,125

### Model C: Hybrid Quantum-Classical CNN
- Input: 4 classical latent features
- Scaled via $\tanh(\mathbf{x}) \cdot \pi \in [-\pi, \pi]$
- 4-Qubit Variational Quantum Circuit (Angle embedding + rotation layers + ring entanglement)
- 4 Pauli-$Z$ expectation measurements $\in [-1.0, 1.0]$
- Classical Readout: $\text{Linear}(4 \to 1)$
- **Total Parameters**: 11,105 (Backbone: 11,100, Quantum Weights: 24, Readout: 5)

---

## 8. Quantum Feature Encoding

The 4 continuous outputs $\mathbf{x} = [x_0, x_1, x_2, x_3]$ from the classical projection layer are mapped to qubit rotation angles via smooth scaling:

$$\theta_i = \pi \cdot \tanh(x_i), \quad \theta_i \in (-\pi, \pi)$$

Features are encoded into the 4 qubits using **$Y$-axis Angle Embedding**:

$$U_{\text{enc}}(\boldsymbol{\theta}) = \bigotimes_{i=0}^3 R_y(\theta_i) = \bigotimes_{i=0}^3 \exp\left(-i \frac{\theta_i}{2} Y\right)$$

Starting from the reference ground state $|0\rangle^{\otimes 4}$, the encoded state becomes:

$$|\psi_0\rangle = U_{\text{enc}}(\boldsymbol{\theta}) |0000\rangle$$

---

## 9. Variational Quantum Circuit

The parameterized variational quantum circuit (VQC) executes $L$ parameterized layers (baseline $L=2$; ablation $L=1$). 

For each layer $l \in \{1, \dots, L\}$ and qubit $q \in \{0, 1, 2, 3\}$, arbitrary single-qubit rotations are parameterized by trainable Euler-style rotation angles:

$$U_{\text{rot}}^{(l, q)} = R_z(\omega_{l, q, 2}) \cdot R_y(\omega_{l, q, 1}) \cdot R_x(\omega_{l, q, 0})$$

where $\boldsymbol{\omega} \in \mathbb{R}^{L \times 4 \times 3}$ is initialized from standard normal distributions and updated end-to-end via PyTorch backpropagation.

---

## 10. Entanglement Topology

To generate multi-qubit quantum correlations and represent non-linear feature interactions, a **closed ring topology** of Controlled-NOT ($\text{CNOT}$) gates is executed after the rotation gates in each layer:

$$\text{CNOT}(0, 1) \to \text{CNOT}(1, 2) \to \text{CNOT}(2, 3) \to \text{CNOT}(3, 0)$$

This creates circular entanglement across all 4 qubits, guaranteeing that each qubit state depends on its neighbors without introducing deep gate hierarchies.

---

## 11. Quantum Measurement & Readout

At the conclusion of the circuit, expectation values of the Pauli-$Z$ observable are measured on each qubit:

$$\langle Z_q \rangle = \langle \psi_{\text{final}} | Z_q | \psi_{\text{final}} \rangle \in [-1.0, 1.0], \quad q \in \{0, 1, 2, 3\}$$

The 4 expectation values $\mathbf{z} = [\langle Z_0 \rangle, \langle Z_1 \rangle, \langle Z_2 \rangle, \langle Z_3 \rangle]^T$ are passed into a trainable linear layer:

$$\hat{y}_{\text{logit}} = \mathbf{w}^T \mathbf{z} + b$$

The final class probability is obtained via the standard sigmoid activation $\sigma(\hat{y}_{\text{logit}})$.

---

## 12. Training Methodology & Imbalance Mitigation

- **Optimizer**: Adam ($\text{lr} = 0.001$, $\text{weight\_decay} = 10^{-4}$)
- **Batch Size**: 64
- **Random Seed**: Single fixed seed (`seed = 42`). Note that multi-seed evaluation (e.g., training over 5 or 10 independent seeds with mean and standard deviation) was not performed.
- **Max Epochs**: 25 with early stopping patience of 5 epochs on validation loss
- **Learning Rate Scheduler**: `ReduceLROnPlateau` ($\text{mode}=\text{'min'}$, $\text{factor}=0.5$, $\text{patience}=2$)
- **Class Imbalance Mitigation (`pos_weight`)**:
  Pneumonia (class `1`) constitutes the **majority class** in the training set ($N_{\text{pos}} = 3494$, $N_{\text{neg}} = 1214$; $74.21\%$ positive). We compute the training positive class weight as:
  
  $$\text{pos\_weight} = \frac{N_{\text{neg}}}{N_{\text{pos}}} = \frac{1214}{3494} \approx 0.3475$$
  
  Applied directly inside `torch.nn.BCEWithLogitsLoss(pos_weight=0.3475)`. Because $\text{pos\_weight} < 1.0$, this **reduces** the relative loss and gradient contribution of majority positive examples to balance class contributions, rather than specifically encouraging higher pneumonia recall. The high recall ($\sim 95\% - 98\%$) observed across all trained models is an empirical finding, not an intended direct effect of this downweighting. Validation and test partitions are never altered or resampled.
- **Differentiable Simulation**: PennyLane `TorchLayer` using analytical `backprop` gradient calculation on the `default.qubit` backend.

---

## 13. Evaluation Metrics

Evaluations are performed on the official held-out test partition ($N=624$) at the standard classification threshold $\tau = 0.5$:

- **Accuracy**: $\frac{TP + TN}{TP + TN + FP + FN}$
- **Precision / PPV**: $\frac{TP}{TP + FP}$
- **Recall / Sensitivity**: $\frac{TP}{TP + FN}$
- **Specificity / TNR**: $\frac{TN}{TN + FP}$
- **$F_1$-Score**: $2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$
- **ROC-AUC**: Area Under the Receiver Operating Characteristic Curve
- **Inference Latency**: Total execution time and per-image latency (ms/image) on CPU simulation.

---

## 14. Experimental Results & Comparison

Below are the actual experimental results obtained from training and evaluating all models on the official held-out PneumoniaMNIST test set ($N=624$):

| Metric | Classical CNN | CNN + MLP (Control) | Hybrid QNN (2-Layer) | Hybrid QNN (1-Layer) |
| :--- | :---: | :---: | :---: | :---: |
| **Accuracy** | 85.74% | 87.66% | **89.10%** | **90.38%** |
| **Precision** | 0.8237 | 0.8648 | 0.8710 | **0.8873** |
| **Recall (Sensitivity)** | **0.9821** | 0.9513 | 0.9692 | 0.9692 |
| **Specificity** | 0.6496 | 0.7521 | 0.7607 | **0.7949** |
| **$F_1$-Score** | 0.8959 | 0.9060 | 0.9175 | **0.9265** |
| **ROC-AUC** | 0.9288 | 0.9235 | 0.9374 | **0.9407** |
| **Training Time** | 16.49s (19 ep) | **11.90s (14 ep)** | 28.84s (25 ep) | 26.38s (25 ep) |
| **Test Inference Time (624 imgs)** | **0.03s** | **0.03s** | 0.05s | 0.04s |
| **Amortized Batch Latency** | **0.04 ms/img** | **0.04 ms/img** | 0.07 ms/img | 0.06 ms/img |
| **Total Parameters** | 105,281 | 11,125 | **11,105** | **11,093** |

*Note: Latency is reported as amortized throughput under batch size 64 on CPU, not sequential single-image latency.*

### Key Scientific Findings:
1. **Competitive Accuracy**: Both Hybrid QNN configurations achieved higher test accuracy (89.10% and 90.38%) and higher $F_1$-scores (0.9175 and 0.9265) than the Classical CNN baseline (85.74%, $F_1=0.8959$) and the CNN + MLP control (87.66%, $F_1=0.9060$).
2. **Improved Specificity**: The quantum circuits significantly enhanced model specificity ($76.07\%$ and $79.49\%$) compared to the baseline CNN ($64.96\%$), reducing false positives while maintaining clinical sensitivity above $96.9\%$.
3. **Parameter Efficiency**: The Hybrid QNN achieves this performance with nearly **$10\times$ fewer parameters** (11,105 vs 105,281) than the full classical CNN.
4. **Honest Caveat**: The classical control (CNN + MLP) also achieved 87.66% accuracy with only 11,125 parameters, showing that bottlenecking the CNN to 4 latent dimensions is an effective regularizer. The quantum layer provides a modest empirical boost (~1.4% - 2.7% accuracy), but does **not** represent a quantum supremacy or computational advantage.

### 14.1 Analysis of the Validation-to-Test Performance Gap
Across all architectures, test accuracy is lower than validation accuracy (e.g., 2-Layer QNN: $95.80\% \to 89.10\%$; Classical CNN: $95.80\% \to 85.74\%$). A rigorous inspection reveals that two intertwined factors contribute to this observed drop:
1. **Prevalence Shift in Test Split**: The test set features a substantially higher proportion of Normal images ($37.50\%$) compared to the validation set ($25.76\%$) and training set ($25.79\%$).
2. **Substantial Drop in Test Specificity**: While recall on pneumonia cases remains consistently high across partitions ($95.63\% \to 96.92\%$ for the 2-layer QNN), test specificity drops sharply compared to validation specificity ($96.30\% \to 76.07\%$ in the QNN; $94.07\% \to 64.96\%$ in the Classical CNN).
3. **Combined Effect**: The class distribution difference alters how false positives affect overall accuracy, but it does not independently explain the drop. The substantial increase in false positives on test normal cases indicates genuine diagnostic ambiguity or distribution shift in the test images. Both the prevalence shift and the lower specificity on test normal cases contribute to the lower test accuracy.

---

## 15. Ablation Experiments: One-Layer vs. Two-Layer Variational Circuit

We conducted a controlled ablation on the depth of the variational quantum circuit:
- **Primary Configuration (2-Layer VQC)**: 4 Qubits, 2 Variational Layers (24 rotation parameters). Selected as the primary model based on validation metrics.
- **Ablation Configuration (1-Layer VQC)**: 4 Qubits, 1 Variational Layer (12 rotation parameters).

### Validation vs. Test Ablation Comparison:

| Metric | 1-Layer VQC (Ablation) | 2-Layer VQC (Primary) | Delta ($\Delta$) |
| :--- | :---: | :---: | :---: |
| **Validation Loss (Best)** | 0.0584 | **0.0557** | -0.0027 (2-L better) |
| **Validation Accuracy (Best Checkpoint)** | 95.61% | **95.80%** | +0.19% (2-L better) |
| **Validation $F_1$ (Best Checkpoint)** | 0.9699 | **0.9713** | +0.0014 (2-L better) |
| **Held-out Test Accuracy** | **90.38%** | 89.10% | +1.28% (1-L higher in this run) |
| **Test Precision** | **0.8873** | 0.8710 | +0.0163 |
| **Test Recall** | 0.9692 | 0.9692 | 0.0000 |
| **Test Specificity** | **0.7949** | 0.7607 | +0.0342 |
| **Test $F_1$-Score** | **0.9265** | 0.9175 | +0.0090 |
| **Test ROC-AUC** | **0.9407** | 0.9374 | +0.0033 |
| **Total Training Time** | **26.38s (25 ep)** | 28.84s (25 ep) | -2.46s |
| **Amortized Batch Latency** | **0.06 ms/img** | 0.07 ms/img | -0.01 ms/img |

### Methodological Interpretation:
- **Model Presentation**: The 2-layer model is retained as the **primary model architecture** because it was selected on validation data (achieving lower validation loss and higher validation accuracy). The 1-layer model is presented strictly as an **ablation experiment**.
- **Test Set Observation**: While the 1-layer model achieved a higher test accuracy in this particular training run ($90.38\%$ vs $89.10\%$), this difference corresponds to only 8 out of 624 test images ($564$ vs $556$ correct).
- **No Definitive Superiority Claim**: A paired McNemar test on the test set predictions reveals that the difference between the 1-layer and 2-layer configurations is **not statistically significant** ($\chi^2 = 1.7500, p = 0.1859$, $p > 0.05$). We therefore do **not** claim that one layer is definitively superior; rather, both depths yield comparable representation capacity on this 4-dimensional latent space.

---

## 16. Limitations & Scientific Nuances

1. **No Demonstrated Quantum Advantage**: The 4-qubit circuit runs entirely on a classical state-vector simulator (`default.qubit`) on CPU. The project demonstrates quantum-classical neural network integration and parameter efficiency, **not** quantum computational speedup or general superiority over modern classical deep learning.
2. **Statistical Comparisons Against Classical Control**: 
   - A paired McNemar test on the held-out test set reveals that the primary 2-layer QNN does **not** significantly outperform the matched classical CNN + MLP control ($\chi^2 = 1.9394, p = 0.1637$).
   - The 1-layer ablation QNN does exhibit a statistically significant difference against the classical control in this run ($\chi^2 = 9.4815, p = 0.0021$), but this constitutes evidence from a single seed.
3. **Single Random Seed**: All models were trained and evaluated using a single fixed seed (`seed = 42`). While fully reproducible from the repository checkpoints, multi-seed evaluation (e.g., reporting mean $\pm$ standard deviation across 5 independent seeds) was not performed.
4. **Latency Measurement Scope**: Reported inference latencies ($0.04 - 0.07$ ms/img) represent **amortized throughput under batch size 64 on CPU**, which includes batch loading and quantum simulation. Sequential single-image latency (batch size 1) is higher due to per-call Python overhead.
5. **Simulator vs. Physical Hardware**: Physical quantum processors (QPUs) suffer from gate infidelities, readout noise, and qubit decoherence, which are absent in state-vector simulation.
6. **Clinical Non-Readiness**: This study investigates academic proof-of-concept architectures on downsampled ($28 \times 28$) radiographs and is not intended for clinical diagnosis.

---

## 17. Reproducibility Instructions

This project uses `uv` for reproducible Python package management and virtual environment execution.

### A. Environment Setup
```bash
# Clone the repository
git clone https://github.com/adityasahrawat/quantum-medical-image-classification.git
cd quantum-medical-image-classification

# Create virtual environment with Python 3.11 using uv
uv venv --python /opt/homebrew/bin/python3.11 .venv
source .venv/bin/activate

# Install all locked dependencies
uv pip install -r pyproject.toml
```

### B. Dataset Download & Verification
```bash
python -c "
from medmnist import PneumoniaMNIST
for s in ['train', 'val', 'test']:
    PneumoniaMNIST(split=s, download=True, root='data')
"
```

### C. Running Unit and Integration Tests
```bash
pytest -v tests/test_pipeline.py
```

### D. Training Models
```bash
# 1. Train Classical CNN (Model A)
python src/training/train_classical.py --model cnn

# 2. Train CNN + MLP Control (Model B)
python src/training/train_classical.py --model classical_hybrid

# 3. Train Hybrid Quantum CNN & Ablation (Model C)
python src/training/train_quantum.py --ablation
```

### E. Comprehensive Test Set Evaluation & Figure Generation
```bash
python src/evaluation/evaluate.py
```
This script computes metrics across all checkpoints on the 624 test images and generates all figures into `outputs/figures/`.

### F. Running Single-Image Inference
```bash
# Run inference on sample Pneumonia image
python src/inference.py --image data/sample_pneumonia.png

# Run inference on sample Normal image
python src/inference.py --image data/sample_normal.png
```

---

## 18. References

1. **MedMNIST v2 Benchmark**: Yang, J., Shi, R., Wei, D., Liu, Z., Zhao, L., Ke, B., ... & Ni, B. (2023). MedMNIST v2-A large-scale lightweight benchmark for 2D and 3D biomedical image classification. *Scientific Data*, 10(1), 41. [https://doi.org/10.1038/s41597-022-01721-8](https://doi.org/10.1038/s41597-022-01721-8)
2. **Pediatric Chest Radiographs**: Kermany, D. S., Goldbaum, M., Cai, W., Valentim, C. C., Liang, H., Baxter, S. L., ... & Zhang, K. (2018). Identifying medical diagnoses and treatable diseases by image-based deep learning. *Cell*, 172(5), 1122-1131.
3. **PennyLane**: Bergholm, V., Izaac, J., Schuld, M., Gogolin, C., Alam, M. S., ... & Killoran, N. (2018). PennyLane: Automatic differentiation and machine learning of quantum computers. *arXiv:1811.04968*.
4. **Quantum Machine Learning**: Schuld, M., & Petruccione, F. (2021). *Machine Learning with Quantum Computers*. Springer Nature.
