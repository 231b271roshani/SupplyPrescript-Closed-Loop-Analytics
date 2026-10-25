"""Generate and prepare the reproducible shipment-delay sample dataset."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_shipments.csv"
RAW_COLUMNS = [
    "shipment_id",
    "supplier",
    "product",
    "order_date",
    "promised_delivery_date",
    "actual_delivery_date",
    "shipping_method",
    "shipping_cost",
    "weather_disruption",
    "port_congestion",
    "supplier_disruption",
]
CATEGORICAL_FEATURES = ["supplier", "product", "shipping_method"]
NUMERIC_FEATURES = [
    "planned_lead_days",
    "shipping_cost",
    "weather_disruption",
    "port_congestion",
    "supplier_disruption",
]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES
TARGET = "is_delayed"


def generate_sample_data(path: Path = DATA_PATH, rows: int = 600, seed: int = 42) -> pd.DataFrame:
    """Write deterministic, fictional shipment records to ``path``."""
    if rows < 20:
        raise ValueError("rows must be at least 20 to support a useful train/test split")

    rng = np.random.default_rng(seed)
    suppliers = np.array(["Northstar", "BluePeak", "CedarWorks", "DeltaSource", "Evergreen"])
    products = np.array(["Microchips", "Sensors", "Motors", "Batteries", "Controllers", "Displays"])
    shipping_methods = np.array(["Ground", "Ocean", "Air"])
    supplier_risk = {"Northstar": 0.1, "BluePeak": 0.35, "CedarWorks": 0.0, "DeltaSource": 0.55, "Evergreen": 0.2}
    method_cost = {"Ground": 450.0, "Ocean": 220.0, "Air": 1250.0}

    supplier = rng.choice(suppliers, rows)
    product = rng.choice(products, rows)
    shipping_method = rng.choice(shipping_methods, rows, p=[0.45, 0.35, 0.20])
    planned_lead_days = rng.integers(5, 36, rows)
    shipping_cost = np.array([method_cost[method] for method in shipping_method])
    shipping_cost = np.round(shipping_cost * rng.uniform(0.8, 1.25, rows), 2)
    weather_disruption = rng.binomial(1, 0.14, rows)
    port_congestion = rng.binomial(1, 0.18, rows)
    supplier_disruption = np.array([rng.binomial(1, supplier_risk[name]) for name in supplier])

    start_date = pd.Timestamp("2024-01-01")
    order_dates = start_date + pd.to_timedelta(rng.integers(0, 730, rows), unit="D")
    promised_dates = order_dates + pd.to_timedelta(planned_lead_days, unit="D")
    supplier_risk_values = np.array([supplier_risk[name] for name in supplier])
    delay_score = (
        -2.2
        + 0.045 * (planned_lead_days - 18)
        + 1.0 * weather_disruption
        + 1.05 * port_congestion
        + 1.25 * supplier_disruption
        + 0.55 * supplier_risk_values
        + 0.35 * (shipping_method == "Ocean")
        - 0.3 * (shipping_method == "Air")
    )
    delay_probability = 1 / (1 + np.exp(-delay_score))
    delayed = rng.binomial(1, delay_probability)
    delay_days = np.where(
        delayed == 1,
        1 + weather_disruption + port_congestion + supplier_disruption + rng.poisson(2, rows),
        0,
    )
    actual_dates = promised_dates + pd.to_timedelta(delay_days, unit="D")

    frame = pd.DataFrame(
        {
            "shipment_id": [f"SP-{index:05d}" for index in range(1, rows + 1)],
            "supplier": supplier,
            "product": product,
            "order_date": order_dates.date,
            "promised_delivery_date": promised_dates.date,
            "actual_delivery_date": actual_dates.date,
            "shipping_method": shipping_method,
            "shipping_cost": shipping_cost,
            "weather_disruption": weather_disruption,
            "port_congestion": port_congestion,
            "supplier_disruption": supplier_disruption,
        }
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return frame


def load_and_prepare_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Validate records, remove duplicate/incomplete rows, and derive targets/features."""
    if not path.exists():
        raise FileNotFoundError(f"Shipment data not found at {path}; generate it with python -m ml.train_model")

    frame = pd.read_csv(path)
    missing_columns = sorted(set(RAW_COLUMNS) - set(frame.columns))
    if missing_columns:
        raise ValueError(f"Shipment data is missing required columns: {', '.join(missing_columns)}")

    frame = frame[RAW_COLUMNS].copy()
    frame = frame.drop_duplicates(subset=["shipment_id"], keep="first")
    for column in ["order_date", "promised_delivery_date", "actual_delivery_date"]:
        frame[column] = pd.to_datetime(frame[column], errors="coerce")
    for column in ["shipping_cost", "weather_disruption", "port_congestion", "supplier_disruption"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame = frame.dropna(subset=RAW_COLUMNS)
    if frame.empty:
        raise ValueError("Shipment data has no complete, valid rows")
    if (frame["shipping_cost"] < 0).any():
        raise ValueError("shipping_cost must be non-negative")
    for column in ["weather_disruption", "port_congestion", "supplier_disruption"]:
        if not frame[column].isin([0, 1]).all():
            raise ValueError(f"{column} must contain only 0 or 1")
    if (frame["promised_delivery_date"] < frame["order_date"]).any():
        raise ValueError("promised_delivery_date cannot be before order_date")

    frame["planned_lead_days"] = (
        frame["promised_delivery_date"] - frame["order_date"]
    ).dt.days
    frame["days_late"] = (
        frame["actual_delivery_date"] - frame["promised_delivery_date"]
    ).dt.days.clip(lower=0)
    frame[TARGET] = (frame["days_late"] > 0).astype(int)
    if frame[TARGET].nunique() < 2:
        raise ValueError("Shipment data must contain both on-time and delayed shipments")
    return frame.reset_index(drop=True)


def shipment_features(record: dict) -> pd.DataFrame:
    """Create the model's pre-outcome feature row from a stored shipment."""
    order_date = pd.Timestamp(record["order_date"])
    promised_date = pd.Timestamp(record["promised_delivery_date"])
    return pd.DataFrame(
        [
            {
                "supplier": record["supplier"],
                "product": record["product"],
                "shipping_method": record["shipping_method"],
                "planned_lead_days": (promised_date - order_date).days,
                "shipping_cost": float(record["shipping_cost"]),
                "weather_disruption": int(record["weather_disruption"]),
                "port_congestion": int(record["port_congestion"]),
                "supplier_disruption": int(record["supplier_disruption"]),
            }
        ],
        columns=FEATURES,
    )
