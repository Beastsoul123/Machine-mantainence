# backend/graph_generator.py

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def generate_machine_graph(machine_id):
    df = pd.read_csv('data/Machine_Maintenance_Dataset.csv')
    chunk_size = len(df) // 12
    chunk = df[(machine_id-1)*chunk_size : machine_id*chunk_size]

    plt.figure(figsize=(6,3), dpi=100)
    plt.plot(chunk['Temperature'], label='Temp', color='#e11d48')
    plt.plot(chunk['Vibration'],   label='Vib',  color='#2563eb')
    plt.plot(chunk['Pressure'],    label='Pres', color='#16a34a')
    plt.plot(chunk['Humidity'],    label='Hum',  color='#f59e0b')
    plt.legend(loc='upper right')
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf
