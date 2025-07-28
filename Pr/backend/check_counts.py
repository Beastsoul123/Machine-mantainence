# check_counts.py

from app import app
from models import Machine, SensorReading

with app.app_context():
    print("Machines:", Machine.query.count())
    print("Readings:", SensorReading.query.count())
