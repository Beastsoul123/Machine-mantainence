# ingest_readings.py

import os
from datetime import datetime
import pandas as pd

from app import app, db
from models import Machine, SensorReading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'Machine_Maintenance_Dataset.csv')

with app.app_context():
    # 1) Clear out old readings
    deleted = db.session.query(SensorReading).delete()
    print(f"Cleared {deleted} old readings")

    # 2) Load CSV & compute chunk size
    df       = pd.read_csv(CSV_PATH)
    machines = Machine.query.all()
    n        = len(machines)
    chunk_sz = len(df) // n if n else 0
    print(f"CSV rows: {len(df)}, Machines: {n}, chunk size: {chunk_sz}")

    # 3) Insert one latest reading per machine
    inserted = 0
    for idx, machine in enumerate(machines):
        start    = idx * chunk_sz
        end      = start + chunk_sz
        slice_df = df.iloc[start:end] if chunk_sz > 0 else df

        if slice_df.empty:
            print(f"  ⚠️ chunk {idx} empty, skipping machine {machine.id}")
            continue

        row = slice_df.iloc[-1]
        reading = SensorReading(
            machine_id            = machine.id,
            timestamp             = datetime.utcnow(),
            temperature           = float(row['Temperature']),
            vibration             = float(row['Vibration']),
            pressure              = float(row['Pressure']),
            humidity              = float(row['Humidity']),
            sound_level           = float(row['SoundLevel']),
            operating_hours       = float(row['OperatingHours']),
            last_maintenance_days = float(row['LastMaintenanceDays'])
        )
        db.session.add(reading)
        inserted += 1

    # 4) Commit all at once
    db.session.commit()
    print(f"✅ Inserted {inserted} new readings")
