"""FastAPI application for shipment lookup and delay prediction."""

from __future__ import annotations

import os
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ml.data import DATA_PATH, shipment_features
from ml.train_model import MODEL_PATH

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = Path(os.environ.get("SUPPLYPRESCRIPT_DB", PROJECT_ROOT / "data" / "supplyprescript.db"))


class ShipmentPrediction(BaseModel):
    shipment_id: str
    supplier: str
    product: str
    shipping_method: str
    promised_delivery_date: str
    actual_delivery_date: str
    is_delayed: bool
    delay_probability: float
    actual_days_late: int


def initialize_database(database_path: Path, data_path: Path) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS shipments (
                shipment_id TEXT PRIMARY KEY,
                supplier TEXT NOT NULL,
                product TEXT NOT NULL,
                order_date TEXT NOT NULL,
                promised_delivery_date TEXT NOT NULL,
                actual_delivery_date TEXT NOT NULL,
                shipping_method TEXT NOT NULL,
                shipping_cost REAL NOT NULL,
                weather_disruption INTEGER NOT NULL,
                port_congestion INTEGER NOT NULL,
                supplier_disruption INTEGER NOT NULL
            )
            """
        )
        if data_path.exists():
            frame = pd.read_csv(data_path)
            columns = [
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
            frame = frame[columns].drop_duplicates(subset=["shipment_id"])
            connection.executemany(
                """
                INSERT OR IGNORE INTO shipments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                frame.itertuples(index=False, name=None),
            )


def create_app(
    database_path: Path = DATABASE_PATH,
    data_path: Path = DATA_PATH,
    model_path: Path = MODEL_PATH,
) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        initialize_database(database_path, data_path)
        yield

    app = FastAPI(title="SupplyPrescript", version="0.1.0", lifespan=lifespan)

    @app.get("/", response_class=HTMLResponse)
    def shipment_lookup() -> str:
        return """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>SupplyPrescript | Shipment lookup</title>
<style>
body{font:16px system-ui,sans-serif;max-width:760px;margin:4rem auto;padding:0 1rem;color:#172b4d}
main{border:1px solid #d8dee9;border-radius:12px;padding:2rem}
input,button{font:inherit;padding:.65rem;border:1px solid #aab5c5;border-radius:6px}
button{background:#155eef;color:white;border:0;cursor:pointer;margin-left:.4rem}
pre{white-space:pre-wrap;background:#f5f7fa;padding:1rem;border-radius:6px}
</style></head>
<body><main><h1>Shipment delay lookup</h1>
<p>Enter a shipment ID to see its stored details and baseline delay prediction.</p>
<form id="lookup"><label for="shipment-id">Shipment ID</label>
<input id="shipment-id" placeholder="SP-00001" required>
<button>Predict delay</button></form><pre id="result" aria-live="polite"></pre>
<script>
document.querySelector("#lookup").addEventListener("submit", async event => {
  event.preventDefault();
  const id = document.querySelector("#shipment-id").value.trim();
  const result = document.querySelector("#result");
  result.textContent = "Loading...";
  try {
    const response = await fetch(`/api/shipments/${encodeURIComponent(id)}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Shipment lookup failed");
    result.textContent = JSON.stringify(data, null, 2);
  } catch (error) { result.textContent = error.message; }
});
</script></main></body></html>"""

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "model_available": model_path.is_file()}

    @app.get("/api/shipments")
    def list_shipments(limit: Annotated[int, Query(ge=1, le=100)] = 25) -> list[dict]:
        with sqlite3.connect(database_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT shipment_id, supplier, product, shipping_method, promised_delivery_date
                FROM shipments ORDER BY shipment_id LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    @app.get("/api/shipments/{shipment_id}", response_model=ShipmentPrediction)
    def predict_shipment(shipment_id: str) -> ShipmentPrediction:
        with sqlite3.connect(database_path) as connection:
            connection.row_factory = sqlite3.Row
            record = connection.execute(
                "SELECT * FROM shipments WHERE shipment_id = ?", (shipment_id,)
            ).fetchone()
        if record is None:
            raise HTTPException(status_code=404, detail="Shipment not found")
        if not model_path.is_file():
            raise HTTPException(
                status_code=503,
                detail="Delay model is not trained; run python -m ml.train_model first",
            )

        model = joblib.load(model_path)
        features = shipment_features(dict(record))
        delayed = bool(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0, 1])
        promised = pd.Timestamp(record["promised_delivery_date"])
        actual = pd.Timestamp(record["actual_delivery_date"])
        return ShipmentPrediction(
            shipment_id=record["shipment_id"],
            supplier=record["supplier"],
            product=record["product"],
            shipping_method=record["shipping_method"],
            promised_delivery_date=promised.date().isoformat(),
            actual_delivery_date=actual.date().isoformat(),
            is_delayed=delayed,
            delay_probability=round(probability, 4),
            actual_days_late=max((actual - promised).days, 0),
        )

    return app


app = create_app()
