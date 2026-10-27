import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)
n = 1500

supplier_reliability = rng.uniform(0.65, 1.0, n)
distance_km = rng.integers(100, 5000, n)
weather_severity = rng.integers(0, 4, n)
customs_delay_days = rng.integers(0, 6, n)
inventory_level = rng.integers(10, 500, n)

shipping_mode = rng.choice(
    ["Air", "Road", "Sea"], n, p=[0.25, 0.50, 0.25]
)

mode_delay = np.select(
    [shipping_mode == "Air", shipping_mode == "Road"],
    [1.0, 3.0],
    default=6.0
)

delay = (
    mode_delay
    + distance_km / 1200
    + weather_severity * 1.5
    + customs_delay_days
    + (1 - supplier_reliability) * 12
    + rng.normal(0, 1.5, n)
)

delay = np.maximum(0, np.round(delay)).astype(int)

df = pd.DataFrame({
    "supplier_reliability": supplier_reliability.round(3),
    "distance_km": distance_km,
    "weather_severity": weather_severity,
    "customs_delay_days": customs_delay_days,
    "inventory_level": inventory_level,
    "shipping_mode": shipping_mode,
    "actual_delay_days": delay
})

project_dir = Path.cwd().parent
data_dir = project_dir / "data"
data_dir.mkdir(parents=True, exist_ok=True)

output_file = data_dir / "shipments.csv"
df.to_csv(output_file, index=False)

print("Dataset created successfully!")
print("File:", output_file)
print("Total shipments:", len(df))
print(df.head())
