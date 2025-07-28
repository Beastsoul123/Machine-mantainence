import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the dataset
df = pd.read_csv('data/Machine_Maintenance_Dataset.csv')

# Create output folder if not exists
output_folder = '../frontend/assets/graphs'
os.makedirs(output_folder, exist_ok=True)

# Total machines to simulate
num_machines = 12

# Split data into chunks
chunk_size = len(df) // num_machines
machine_dfs = [df[i*chunk_size:(i+1)*chunk_size] for i in range(num_machines)]

# Generate graphs
for i, machine_df in enumerate(machine_dfs):
    machine_name = f"Machine {i+1}"
    plt.figure(figsize=(10, 5))
    
    plt.plot(machine_df['Temperature'], label='Temperature')
    plt.plot(machine_df['Vibration'], label='Vibration')
    plt.plot(machine_df['Pressure'], label='Pressure')
    plt.plot(machine_df['Humidity'], label='Humidity')
    
    plt.title(f'{machine_name} Sensor Data')
    plt.xlabel('Time')
    plt.ylabel('Sensor Values')
    plt.legend()
    
    # Save graph to assets
    graph_filename = f'{output_folder}/graph_{i+1}.png'
    plt.savefig(graph_filename)
    plt.close()

print("Graphs generated and saved to frontend/assets/graphs/")
