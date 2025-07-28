# app.py

import os
import pickle
import joblib
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO

from flask import (
    Flask,
    jsonify,
    request,            # ← added
    abort,
    send_from_directory,
    send_file
)
from flask_migrate import Migrate

from models import db, Machine, ChecklistItem, HazardItem, SensorReading
from graph_generator import generate_machine_graph

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '../frontend')
MODEL_DIR    = os.path.join(BASE_DIR, 'model')

# ── Flask App & Database Setup ────────────────────────────────────────────────
app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=''
)
app.config['SQLALCHEMY_DATABASE_URI']       = 'sqlite:///' + os.path.join(BASE_DIR, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# ── Load ML Artifacts ─────────────────────────────────────────────────────────
scaler  = pickle.load(open(os.path.join(MODEL_DIR, 'scaler.pkl'),        'rb'))
model   = pickle.load(open(os.path.join(MODEL_DIR, 'trained_model.pkl'), 'rb'))
encoder = joblib.load(open(os.path.join(MODEL_DIR, 'encoder.pkl'),      'rb'))

# ── Helper: Compute Hazard & Status ───────────────────────────────────────────
def compute_machine_metrics(machine_id):
    reading = (
        SensorReading.query
            .filter_by(machine_id=machine_id)
            .order_by(SensorReading.timestamp.desc())
            .first()
    )
    if not reading:
        return {'hazard': 0, 'status': 'Unknown'}

    # build DataFrame matching scaler.feature_names_in_
    feature_names = list(scaler.feature_names_in_)
    row = [
        reading.temperature,
        reading.vibration,
        reading.pressure,
        reading.humidity,
        reading.sound_level,
        reading.operating_hours,
        reading.last_maintenance_days
    ]
    df_row = pd.DataFrame([row], columns=feature_names)

    # scale & predict
    X_scaled = scaler.transform(df_row)
    proba    = model.predict_proba(X_scaled)[0]

    # hazard % = highest class-probability × 100
    hazard = int(proba.max() * 100)

    # map to status bucket
    if   hazard >= 90: status = 'MonitorClosely'
    elif hazard >= 30: status = 'NeedsMaintenance'
    else:              status = 'Healthy'

    return {'hazard': hazard, 'status': status}

# ── API: All Machines with Live Metrics ────────────────────────────────────────
@app.route('/api/machines')
def get_machine_data():
    machines = Machine.query.all()
    result   = []

    for m in machines:
        # core record
        rec = {
            'id':                   m.id,
            'name':                 m.name,
            'details':              m.details,
            'image':                m.image,
            'graph':                m.graph,
            'lastMaintenanceDate':  m.last_maintained.isoformat(),
            'nextDueDate':          m.next_due.isoformat()
        }

        # hazard & status
        metrics       = compute_machine_metrics(m.id)
        rec['hazard'] = metrics['hazard']
        rec['status'] = metrics['status']

        # checklist items (include id)
        rec['checklist'] = [
            {
                'id':   item.id,
                'task': item.task,
                'done': item.done
            }
            for item in ChecklistItem.query.filter_by(machine_id=m.id)
        ]

        # hazard descriptions
        rec['hazardList'] = [
            hz.description
            for hz in HazardItem.query.filter_by(machine_id=m.id)
        ]

        result.append(rec)

    return jsonify(result)

# ── API: Time-Series Metrics for Chart.js ────────────────────────────────────
@app.route('/api/machines/<int:machine_id>/metrics')
def get_machine_metrics(machine_id):
    since    = datetime.utcnow() - timedelta(hours=24)
    readings = (
        SensorReading.query
            .filter_by(machine_id=machine_id)
            .filter(SensorReading.timestamp >= since)
            .order_by(SensorReading.timestamp)
            .all()
    )

    data = [{
        't':                   r.timestamp.isoformat(),
        'Temperature':         r.temperature,
        'Vibration':           r.vibration,
        'Pressure':            r.pressure,
        'Humidity':            r.humidity,
        'SoundLevel':          r.sound_level,
        'OperatingHours':      r.operating_hours,
        'LastMaintenanceDays': r.last_maintenance_days
    } for r in readings]

    return jsonify(data)

# ── API: Dynamic PNG Graph via Matplotlib ─────────────────────────────────────
@app.route('/api/machines/<int:machine_id>/graph.png')
def machine_graph(machine_id):
    """
    Generate and return a PNG chart for machine_id on the fly.
    """
    buf = generate_machine_graph(machine_id)
    return send_file(buf, mimetype='image/png')

# ── New: Toggle Checklist Item State ─────────────────────────────────────────
@app.route(
    '/api/machines/<int:machine_id>/checklist/<int:item_id>',
    methods=['PUT']
)
def toggle_checklist_item(machine_id, item_id):
    item = ChecklistItem.query.get_or_404(item_id)
    # ensure it belongs to this machine
    if item.machine_id != machine_id:
        abort(404)

    data = request.get_json() or {}
    if 'done' not in data:
        return jsonify({'error': 'Missing "done" flag'}), 400

    item.done = bool(data['done'])
    db.session.commit()
    return jsonify({'id': item.id, 'done': item.done})

# ── Serve SPA Entrypoint & Static Files ───────────────────────────────────────
@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    # prevent API catch-all
    if filename.startswith('api/'):
        abort(404)

    file_path = os.path.join(FRONTEND_DIR, filename)
    if not os.path.realpath(file_path).startswith(os.path.realpath(FRONTEND_DIR)):
        abort(403)
    if os.path.isfile(file_path):
        return send_from_directory(FRONTEND_DIR, filename)
    abort(404)

# ── Launch ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
    