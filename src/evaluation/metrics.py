"""
Comprehensive classification metrics calculation for medical image diagnosis.
"""
from typing import Dict, Tuple, Optional
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
)


def compute_classification_metrics(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float = 0.5,
) -> Dict:
    """
    Compute full classification metrics at a given decision threshold.

    Required metrics:
    - Accuracy
    - Precision
    - Recall (Sensitivity)
    - Specificity (True Negative Rate)
    - F1-Score
    - ROC-AUC
    - Confusion Matrix (TN, FP, FN, TP)

    Args:
        y_true: Ground truth binary labels (0 or 1).
        y_prob: Predicted probabilities for the positive class (Pneumonia = 1).
        threshold: Classification decision threshold (default: 0.5).

    Returns:
        Dictionary containing all metrics and confusion matrix elements.
    """
    y_true = np.asarray(y_true).astype(int).ravel()
    y_prob = np.asarray(y_prob).astype(float).ravel()
    y_pred = (y_prob >= threshold).astype(int)

    # Confusion matrix: [[TN, FP], [FN, TP]]
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)  # Sensitivity
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    f1 = f1_score(y_true, y_pred, zero_division=0)

    try:
        roc_auc = roc_auc_score(y_true, y_prob)
    except ValueError:
        roc_auc = 0.5

    return {
        "threshold": float(threshold),
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "sensitivity": float(recall),
        "specificity": float(specificity),
        "f1": float(f1),
        "roc_auc": float(roc_auc),
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
            "matrix": cm.tolist(),
        },
    }


def find_optimal_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    criterion: str = "youden",
) -> Tuple[float, float]:
    """
    Find optimal classification threshold on validation set.

    Args:
        y_true: Ground truth validation labels.
        y_prob: Predicted validation probabilities.
        criterion: 'youden' (Sensitivity + Specificity - 1) or 'f1'.

    Returns:
        (best_threshold, best_score)
    """
    y_true = np.asarray(y_true).astype(int).ravel()
    y_prob = np.asarray(y_prob).astype(float).ravel()

    if criterion == "youden":
        fpr, tpr, thresholds = roc_curve(y_true, y_prob)
        j_scores = tpr - fpr
        best_idx = np.argmax(j_scores)
        best_threshold = float(np.clip(thresholds[best_idx], 0.01, 0.99))
        return best_threshold, float(j_scores[best_idx])
    elif criterion == "f1":
        thresholds = np.linspace(0.1, 0.9, 81)
        best_f1 = -1.0
        best_threshold = 0.5
        for t in thresholds:
            pred = (y_prob >= t).astype(int)
            score = f1_score(y_true, pred, zero_division=0)
            if score > best_f1:
                best_f1 = score
                best_threshold = float(t)
        return best_threshold, float(best_f1)
    else:
        raise ValueError(f"Unknown criterion: {criterion}")
