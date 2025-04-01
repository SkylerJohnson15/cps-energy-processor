import pandas as pd
import dask.dataframe as dd
import os

# Define the absolute path to the data directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_dir = os.path.join(project_root, "data")
csv_path = os.path.join(data_dir, "sample_meter_data.csv")

def ingest_file(file_path):
    df = dd.read_csv(file_path)  # Use Dask for large files
    return df.compute()  # Convert to Pandas

if __name__ == "__main__":
    data = ingest_file(csv_path)
    print(data.head())