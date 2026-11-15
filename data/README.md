# PneumoniaMNIST Dataset

## Overview

The dataset used in this project is **PneumoniaMNIST**, part of the official [MedMNIST v2](https://medmnist.com/) benchmark:
- Reference: Yang, J., Shi, R., Wei, D., Liu, Z., Zhao, L., Ke, B., ... & Ni, B. (2023). MedMNIST v2-A large-scale lightweight benchmark for 2D and 3D biomedical image classification. *Scientific Data*, 10(1), 41.

PneumoniaMNIST is derived from the pediatric chest X-ray dataset originally published by Kermany et al. (2018). It comprises low-resolution (28 × 28) grayscale chest radiographs for binary classification between **Normal** and **Pneumonia**.

## Dataset Properties

- **Total Images**: 5,856
- **Resolution**: 28 × 28 pixels
- **Channels**: 1 (Grayscale)
- **Task**: Binary Classification
- **Classes**:
  - `0`: Normal (Healthy chest X-ray)
  - `1`: Pneumonia (Bacterial or viral pneumonia)

## Official Partitions & Class Distribution

| Partition | Normal (`0`) | Pneumonia (`1`) | Total | Normal % | Pneumonia % |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Train** | 1,214 | 3,494 | **4,708** | 25.79% | 74.21% |
| **Validation** | 135 | 389 | **524** | 25.76% | 74.24% |
| **Test** | 234 | 390 | **624** | 37.50% | 62.50% |
| **Overall** | 1,583 | 4,273 | **5,856** | 27.03% | 72.97% |

## Preprocessing & Class Imbalance Handling

- Pixel intensities are normalized to the standard range $[0, 1]$ via `transforms.ToTensor()`.
- Training data is augmented with mild rotations ($\le 5^\circ$), small translations ($\le 5\%$), and mild brightness/contrast jittering.
- Validation and test sets are strictly unaugmented.
- The training set class imbalance (Pneumonia constitutes the majority class with 3,494 vs. 1,214 normal cases) is addressed using `pos_weight = 1214 / 3494 ≈ 0.3475` in `BCEWithLogitsLoss`. Because $\text{pos\_weight} < 1.0$, this downweights the loss contribution of majority positive samples to balance gradient contributions between classes, rather than artificially inflating positive recall. Validation and test splits are never rebalanced.
- Note on partition shifts: The test set has a significantly higher proportion of Normal cases (37.50% vs 25.76% in validation), which changes the impact of false positives on overall test accuracy.
