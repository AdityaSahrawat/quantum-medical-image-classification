"""
Evaluation metrics and visualization package
"""
from src.evaluation.metrics import compute_classification_metrics, find_optimal_threshold
from src.evaluation.visualization import (
    plot_dataset_samples,
    plot_class_distribution,
    plot_training_curves,
    plot_confusion_matrices,
    plot_combined_roc_curves,
    plot_model_comparison_bar,
    plot_prediction_samples,
    save_quantum_circuit_diagram,
)

__all__ = [
    "compute_classification_metrics",
    "find_optimal_threshold",
    "plot_dataset_samples",
    "plot_class_distribution",
    "plot_training_curves",
    "plot_confusion_matrices",
    "plot_combined_roc_curves",
    "plot_model_comparison_bar",
    "plot_prediction_samples",
    "save_quantum_circuit_diagram",
]
