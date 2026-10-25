import json

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from backend.main import create_app
from ml.data import FEATURES, generate_sample_data, load_and_prepare_data, shipment_features
from ml.train_model import train_model


def test_sample_data_is_reproducible_and_targets_are_derived(tmp_path):
    first_path = tmp_path / "first.csv"
    second_path = tmp_path / "second.csv"
    generate_sample_data(first_path, rows=80)
    generate_sample_data(second_path, rows=80)

    pd.testing.assert_frame_equal(pd.read_csv(first_path), pd.read_csv(second_path))
    prepared = load_and_prepare_data(first_path)
    assert prepared["is_delayed"].equals((prepared["days_late"] > 0).astype(int))
    assert set(prepared["is_delayed"]) == {0, 1}
    assert "actual_delivery_date" not in FEATURES


def test_data_cleaning_deduplicates_and_rejects_bad_cost(tmp_path):
    path = tmp_path / "shipments.csv"
    generate_sample_data(path, rows=80)
    frame = pd.read_csv(path)
    frame = pd.concat([frame, frame.iloc[[0]]], ignore_index=True)
    frame.to_csv(path, index=False)
    assert len(load_and_prepare_data(path)) == 80

    frame.loc[0, "shipping_cost"] = -1
    frame.to_csv(path, index=False)
    with pytest.raises(ValueError, match="shipping_cost"):
        load_and_prepare_data(path)


def test_training_saves_model_and_metrics(tmp_path):
    data_path = tmp_path / "sample.csv"
    artifact_dir = tmp_path / "artifacts"
    generate_sample_data(data_path, rows=120)

    metrics = train_model(data_path, artifact_dir)

    assert metrics["model"] == "XGBoostClassifier"
    assert 0 <= metrics["f1"] <= 1
    assert (artifact_dir / "delay_model.joblib").is_file()
    assert json.loads((artifact_dir / "metrics.json").read_text()) == metrics


def test_api_lists_shipments_predicts_and_handles_missing_records(tmp_path):
    data_path = tmp_path / "sample.csv"
    database_path = tmp_path / "test.db"
    model_path = tmp_path / "model.joblib"
    generate_sample_data(data_path, rows=80)
    train_model(data_path, tmp_path / "artifacts")
    model_path.write_bytes((tmp_path / "artifacts" / "delay_model.joblib").read_bytes())
    app = create_app(database_path, data_path, model_path)

    with TestClient(app) as client:
        listed = client.get("/api/shipments")
        assert listed.status_code == 200
        assert listed.json()[0]["shipment_id"] == "SP-00001"
        prediction = client.get("/api/shipments/SP-00001")
        assert prediction.status_code == 200
        assert 0 <= prediction.json()["delay_probability"] <= 1
        assert isinstance(prediction.json()["is_delayed"], bool)
        assert client.get("/api/shipments/unknown").status_code == 404
        assert "Shipment delay lookup" in client.get("/").text


def test_api_reports_untrained_model(tmp_path):
    data_path = tmp_path / "sample.csv"
    generate_sample_data(data_path, rows=40)
    app = create_app(tmp_path / "test.db", data_path, tmp_path / "missing.joblib")

    with TestClient(app) as client:
        response = client.get("/api/shipments/SP-00001")
        assert response.status_code == 503
        assert "python -m ml.train_model" in response.json()["detail"]


def test_shipment_feature_builder_uses_only_pre_outcome_fields():
    record = {
        "supplier": "Northstar",
        "product": "Sensors",
        "shipping_method": "Ground",
        "order_date": "2025-01-01",
        "promised_delivery_date": "2025-01-11",
        "shipping_cost": 500,
        "weather_disruption": 1,
        "port_congestion": 0,
        "supplier_disruption": 0,
    }

    features = shipment_features(record)
    assert list(features.columns) == FEATURES
    assert features.loc[0, "planned_lead_days"] == 10
