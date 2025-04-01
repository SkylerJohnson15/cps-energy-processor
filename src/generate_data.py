import pandas as pd
import numpy as np
import os

# Define the absolute path to the data directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_dir = os.path.join(project_root, "data")

# Create the data directory if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

# Path to save the CSV
csv_path = os.path.join(data_dir, "sample_meter_data.csv")

dates = pd.date_range("2025-01-01", periods=100000, freq="h")
data = pd.DataFrame({
    "meter_id": np.random.randint(1000, 9999, 100000),
    "timestamp": dates,
    "usage": np.random.uniform(0, 100, 100000)
})
data.to_csv(csv_path, index=False)
print(f"Sample data generated at: {csv_path}")