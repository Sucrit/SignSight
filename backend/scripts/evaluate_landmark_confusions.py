from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from app.services.landmark_classifier import _top_predictions, load_landmarks_dataset


CONFUSION_FAMILIES: list[tuple[str, list[str]]] = [
    ("I/Y", ["I", "Y"]),
    ("U/V/W", ["U", "V", "W"]),
    ("M/N/T/S/E", ["M", "N", "T", "S", "E"]),
    ("D/K/L", ["D", "K", "L"]),
    ("G/H", ["G", "H"]),
    ("P/Q", ["P", "Q"]),
    ("R/U", ["R", "U"]),
    ("C/O/F", ["C", "O", "F"]),
]


@dataclass
class EvalRow:
    truth: str
    prediction: str


def train_eval_model():
    X, y = load_landmarks_dataset()
    if len(X) == 0:
        raise SystemExit("No landmark samples found.")

    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = SVC(kernel="rbf", probability=True, gamma="scale", C=12)
    model.fit(Xtr, ytr)
    return model, Xte, yte


def evaluate_rows(model: SVC, Xte: np.ndarray, yte: np.ndarray) -> list[EvalRow]:
    rows: list[EvalRow] = []
    for vec, truth in zip(Xte, yte, strict=False):
        top_labels, _ = _top_predictions(model, vec.reshape(1, -1))
        rows.append(EvalRow(truth=str(truth), prediction=str(top_labels[0])))
    return rows


def print_family_report(rows: list[EvalRow], name: str, labels: list[str]) -> None:
    filtered = [row for row in rows if row.truth in labels]
    if not filtered:
        print(f"\n{name}: no samples")
        return

    y_true = [row.truth for row in filtered]
    y_pred = [row.prediction for row in filtered]
    print(f"\n=== {name} ===")
    print(f"subset accuracy: {accuracy_score(y_true, y_pred):.3f}")
    print(classification_report(y_true, y_pred, labels=labels, zero_division=0))
    print("confusion matrix")
    print(confusion_matrix(y_true, y_pred, labels=labels))


def main() -> None:
    model, Xte, yte = train_eval_model()
    rows = evaluate_rows(model, Xte, yte)
    y_true = [row.truth for row in rows]
    y_pred = [row.prediction for row in rows]
    print("Overall holdout accuracy")
    print(f"raw: {accuracy_score(y_true, y_pred):.3f}")

    for family_name, labels in CONFUSION_FAMILIES:
        print_family_report(rows, family_name, labels)


if __name__ == "__main__":
    main()
