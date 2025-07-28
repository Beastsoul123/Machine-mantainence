let metricChart1 = null;
let metricChart2 = null;

document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/machines')
    .then(r => r.json())
    .then(machines => {
      const container = document.getElementById('machine-container');
      machines.forEach(m => {
        const card = document.createElement('div');
        card.className = `card status-${m.status}`;
        card.innerHTML = `
          <img src="/assets/${m.image}" alt="${m.name}">
          <h3>${m.name}</h3>
          <p>Hazard: ${m.hazard}% (${m.status})</p>
        `;
        card.onclick = () => showModal(m);
        container.appendChild(card);
      });
    })
    .catch(console.error);
});

function showModal(machine) {
  document.getElementById('modalTitle').textContent = machine.name;
  document.getElementById('modalDetails').textContent = machine.details;
  document.getElementById('modalLastMaintenance').textContent = machine.lastMaintenanceDate;
  document.getElementById('modalNextDue').textContent = machine.nextDueDate;

  const graphEl = document.getElementById('modalGraph');
  graphEl.onerror = () => {
    graphEl.onerror = null;
    graphEl.src = `/assets/graphs/graph_${machine.id}.png`;
  };
  graphEl.src = `/api/machines/${machine.id}/graph.png?ts=${Date.now()}`;

  document.getElementById('modalHazardPercent').textContent = machine.hazard;
  document.getElementById('modalHazardBar').style.width = machine.hazard + '%';

  const checklistEl = document.getElementById('modalChecklist');
  checklistEl.innerHTML = '';
  machine.checklist.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item.task;
    li.dataset.itemId = item.id;
    li.onclick = () => toggleChecklist(machine.id, item.id, li);
    checklistEl.appendChild(li);
  });

  const hazardListEl = document.getElementById('hazardList');
  hazardListEl.innerHTML = '';
  machine.hazardList.forEach(desc => {
    const li = document.createElement('li');
    li.textContent = desc;
    hazardListEl.appendChild(li);
  });

  fetch(`/api/machines/${machine.id}/metrics`)
    .then(r => r.json())
    .then(points => {
      console.table(points);

      // Inject fallback preview data if empty
    if (points.length === 0) {
  console.warn('⚠️ No sensor data found, showing preview fallback.');
  const now = new Date();
  points = Array.from({ length: 24 }, (_, i) => ({
    t: new Date(now.getTime() - (24 - i) * 60 * 60 * 1000).toISOString(),
    Temperature: 22 + Math.sin(i / 2) + (Math.random() * 0.5),
    Vibration: 0.02 + Math.random() * 0.005,
    Pressure: 1.0 + Math.cos(i / 3) * 0.02,
    Humidity: 45 + Math.floor(Math.random() * 10),
    SoundLevel: 60 + Math.floor(Math.random() * 6)
  }));
}


      const dataTemps = points.map(p => ({ x: new Date(p.t), y: p.Temperature }));
      const dataVibs  = points.map(p => ({ x: new Date(p.t), y: p.Vibration }));
      const dataPres  = points.map(p => ({ x: new Date(p.t), y: p.Pressure }));
      const dataHums  = points.map(p => ({ x: new Date(p.t), y: p.Humidity }));
      const dataSounds= points.map(p => ({ x: new Date(p.t), y: p.SoundLevel }));

      const ctx1 = document.getElementById('metricChart').getContext('2d');
      if (metricChart1) metricChart1.destroy();
      metricChart1 = new Chart(ctx1, {
        type: 'line',
        data: {
          datasets: [
            { label: 'Temperature', data: dataTemps, borderColor: '#e11d48', fill: false },
            { label: 'Vibration',   data: dataVibs,  borderColor: '#2563eb', fill: false },
            { label: 'Pressure',    data: dataPres,  borderColor: '#16a34a', fill: false }
          ]
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'hour',
                tooltipFormat: 'HH:mm'
              },
              ticks: {
                autoSkip: true,
                maxRotation: 0,
                maxTicksLimit: 8
              }
            },
            y: {
              beginAtZero: true
            }
          }
        }
      });

      const ctx2 = document.getElementById('metricChart2').getContext('2d');
      if (metricChart2) metricChart2.destroy();
      metricChart2 = new Chart(ctx2, {
        type: 'line',
        data: {
          datasets: [
            { label: 'Humidity',    data: dataHums,   borderColor: '#f59e0b', fill: false },
            { label: 'Sound Level', data: dataSounds, borderColor: '#8b5cf6', fill: false }
          ]
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'hour',
                tooltipFormat: 'HH:mm'
              },
              ticks: {
                autoSkip: true,
                maxRotation: 0,
                maxTicksLimit: 8
              }
            },
            y: {
              beginAtZero: true
            }
          }
        }
      });
    })
    .catch(console.error);

  document.getElementById('modal').style.display = 'flex';
}

function toggleChecklist(machineId, itemId, liEl) {
  const willBeDone = !liEl.classList.contains('done');
  liEl.classList.toggle('done', willBeDone);

  fetch(`/api/machines/${machineId}/checklist/${itemId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ done: willBeDone })
  })
  .then(res => {
    if (!res.ok) {
      liEl.classList.toggle('done', !willBeDone);
      console.error('Failed to update checklist item');
    }
  })
  .catch(err => {
    liEl.classList.toggle('done', !willBeDone);
    console.error(err);
  });
}

document.getElementById('closeBtn').onclick = () =>
  document.getElementById('modal').style.display = 'none';
