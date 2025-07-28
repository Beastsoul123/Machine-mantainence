# inspect_csv.py

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'Machine_Maintenance_Dataset.csv')

df = pd.read_csv(CSV_PATH)
print("CSV Columns:")
for col in df.columns:
    print("  ‑", col)
