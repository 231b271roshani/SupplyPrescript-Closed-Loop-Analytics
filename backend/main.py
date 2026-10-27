from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "delay_model.joblib"

app = FastAPI(
    title="SupplyPrescript API",
    description="Supply-chain prediction and decision support",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ShipmentInput(BaseModel):
    supplier_reliability: float = Field(ge=0, le=1)
    distance_km: float = Field(gt=0)
    weather_severity: float = Field(ge=0, le=10)
    customs_delay_days: float = Field(ge=0)
    inventory_level: float = Field(ge=0)
    shipping_mode: str


@app.get("/")
def home():
    return {
        "message": "Welcome to SupplyPrescript!",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/shipment-example")
def shipment_example():
    return {
        "shipment_id": "SH001",
        "supplier": "Supplier A",
        "predicted_delay_days": 5,
        "recommended_action": "Evaluate an alternative supplier",
    }


@app.post("/predict-delay")
def predict_delay(shipment: ShipmentInput):
    saved_model = joblib.load(MODEL_PATH)
    model = saved_model["model"]
    features = saved_model["features"]

    shipment_data = pd.DataFrame(
        [shipment.model_dump()]
    )[features]

    prediction = max(
        0.0,
        float(model.predict(shipment_data)[0]),
    )

    if prediction >= 5:
        action = (
            "High risk: evaluate alternative suppliers "
            "or faster shipping."
        )
    elif prediction >= 2:
        action = (
            "Moderate risk: monitor shipment and "
            "prepare contingency plans."
        )
    else:
        action = (
            "Low predicted delay: continue routine monitoring."
        )

    return {
        "predicted_delay_days": round(prediction, 2),
        "recommended_action": action,
    }
