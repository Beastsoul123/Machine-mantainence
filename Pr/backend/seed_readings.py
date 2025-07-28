# backend/seed_readings.py

import random
from datetime import datetime, timedelta
from app import app, db
from models import Machine, SensorReading

def seed_readings():
    with app.app_context():
        # Optional: wipe old readings
        SensorReading.query.delete()
        db.session.commit()

        for m in Machine.query.all():
            readings = []
            now = datetime.utcnow()
            for h in range(24):  # 24 hourly readings
                ts = now - timedelta(hours=23 - h)
                readings.append(SensorReading(
                    machine_id            = m.id,
                    timestamp             = ts,
                    temperature           = round(random.uniform(60, 90), 1),
                    vibration             = round(random.uniform(0.2, 0.8), 2),
                    pressure              = round(random.uniform(30, 70), 1),
                    humidity              = round(random.uniform(40, 60), 1),
                    sound_level           = round(random.uniform(60, 100), 1),
                    operating_hours       = round(random.uniform(100, 500), 1),
                    last_maintenance_days = random.randint(0, 30)
                ))
            db.session.bulk_save_objects(readings)
            db.session.commit()

if __name__ == '__main__':
    seed_readings()
    print("✅ Seeded 24 readings per machine.")
