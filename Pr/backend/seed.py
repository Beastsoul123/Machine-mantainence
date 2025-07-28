# seed.py
import json
from datetime import datetime
from app import app, db
from models import Machine, ChecklistItem, HazardItem

DATA_PATH = 'data/machinedata.json'

with app.app_context():
    # Drop & recreate tables
    db.drop_all()
    db.create_all()

    machines = json.load(open(DATA_PATH))
    for idx, m in enumerate(machines, start=1):
        # Parse lastMaintained date
        lm = datetime.fromisoformat(m['lastMaintained'])

        # Create Machine row
        machine = Machine(
            id=idx,
            name=m['name'],
            details=m['details'],
            image=m['image'],
            graph=m['graph'],
            last_maintained=lm,
            hazard=m['hazard']
        )
        db.session.add(machine)

        # Checklist items
        for item in m['checklist']:
            db.session.add(ChecklistItem(
                machine_id=idx,
                task=item['task'],
                done=item['done']
            ))

        # Hazard descriptions
        for desc in m['hazardList']:
            db.session.add(HazardItem(
                machine_id=idx,
                description=desc
            ))

    db.session.commit()
    print("✅ Database seeded!")
