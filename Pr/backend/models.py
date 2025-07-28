# models.py

from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Machine(db.Model):
    __tablename__ = 'machines'
    id                    = db.Column(db.Integer, primary_key=True)
    name                  = db.Column(db.String(128), nullable=False)
    details               = db.Column(db.Text)
    image                 = db.Column(db.String(256))
    graph                 = db.Column(db.String(256))
    last_maintained       = db.Column(db.Date, default=datetime.utcnow)
    maintenance_interval  = db.Column(db.Integer, default=60)
    hazard                = db.Column(db.Integer, default=0)

    @property
    def next_due(self):
        return self.last_maintained + timedelta(days=self.maintenance_interval)

class ChecklistItem(db.Model):
    __tablename__ = 'checklist_items'
    id         = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'))
    task       = db.Column(db.String(256))
    done       = db.Column(db.Boolean, default=False)

class HazardItem(db.Model):
    __tablename__ = 'hazard_items'
    id          = db.Column(db.Integer, primary_key=True)
    machine_id  = db.Column(db.Integer, db.ForeignKey('machines.id'))
    description = db.Column(db.String(256))

class SensorReading(db.Model):
    __tablename__ = 'sensor_readings'

    id                     = db.Column(db.Integer, primary_key=True)
    machine_id             = db.Column(db.Integer, db.ForeignKey('machines.id'))
    timestamp              = db.Column(db.DateTime, default=datetime.utcnow)

    # Columns must match scaler.feature_names_in_
    temperature            = db.Column('Temperature', db.Float)
    vibration              = db.Column('Vibration', db.Float)
    pressure               = db.Column('Pressure', db.Float)
    humidity               = db.Column('Humidity', db.Float)
    sound_level            = db.Column('SoundLevel', db.Float)
    operating_hours        = db.Column('OperatingHours', db.Float)
    last_maintenance_days  = db.Column('LastMaintenanceDays', db.Float)
