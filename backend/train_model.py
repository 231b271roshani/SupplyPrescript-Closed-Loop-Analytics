
import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "shipments.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

features = [
    "supplier_reliability",
    "distance_km",
    "weather_severity",
    "customs_delay_days",
    "inventory_level",
    "shipping_mode",
]

X = df[features]
y = df["actual_delay_days"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

preprocessor = ColumnTransformer(
    transformers=[
        ("shipping_mode", OneHotEncoder(handle_unknown="ignore"), ["shipping_mode"])
    ],
    remainder="passthrough",
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=100, random_state=42, n_jobs=-1
    )),
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

model_path = MODEL_DIR / "delay_model.joblib"
joblib.dump({"model": model, "features": features}, model_path)

print("Model trained successfully!")
print(f"Training records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")
print(f"Mean Absolute Error: {mae:.2f} days")
print(f"R2 Score: {r2:.3f}")
print(f"Saved model to: {model_path}")
