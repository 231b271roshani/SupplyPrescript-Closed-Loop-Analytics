"""Train and evaluate the baseline shipment delay classifier."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier

from ml.data import (
    CATEGORICAL_FEATURES,
    DATA_PATH,
    FEATURES,
    NUMERIC_FEATURES,
    TARGET,
    generate_sample_data,
    load_and_prepare_data,
)

ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "delay_model.joblib"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"
RANDOM_STATE = 42


def train_model(data_path: Path = DATA_PATH, artifact_dir: Path = ARTIFACT_DIR) -> dict:
    if not data_path.exists():
        generate_sample_data(data_path)
    data = load_and_prepare_data(data_path)
    x_train, x_test, y_train, y_test = train_test_split(
        data[FEATURES],
        data[TARGET],
        test_size=0.25,
        random_state=RANDOM_STATE,
        stratify=data[TARGET],
    )
    preprocessor = ColumnTransformer(
        [
            ("categories", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("numbers", "passthrough", NUMERIC_FEATURES),
        ]
    )
    model = Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                "classifier",
                XGBClassifier(
                    objective="binary:logistic",
                    eval_metric="logloss",
                    n_estimators=120,
                    max_depth=4,
                    learning_rate=0.05,
                    subsample=0.9,
                    colsample_bytree=0.9,
                    random_state=RANDOM_STATE,
                    n_jobs=1,
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]
    metrics = {
        "model": "XGBoostClassifier",
        "random_state": RANDOM_STATE,
        "rows": len(data),
        "train_rows": len(x_train),
        "test_rows": len(x_test),
        "delayed_shipments": int(data[TARGET].sum()),
        "delay_rate": round(float(data[TARGET].mean()), 4),
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
    }
    artifact_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, artifact_dir / MODEL_PATH.name)
    (artifact_dir / METRICS_PATH.name).write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return metrics


if __name__ == "__main__":
    print(json.dumps(train_model(), indent=2))
