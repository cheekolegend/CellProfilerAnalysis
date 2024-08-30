import os
import subprocess
import pandas as pd
from pathlib import Path
from Trackrefiner.strain.processCellProfilerData import process_data
from concurrent.futures import ProcessPoolExecutor

win_path = r'C:\Users\aaron\OneDrive\Documents\ilastik_cp_run\run'
processing_dir = Path(win_path)

output_directory = None # None defaults to output in same directory as tracking csv file
dt = 5/60 # h
min_life_history_of_bacteria = 10/60
growth_rate_method = "Linear Regression"
assigning_cell_type = False
warn = True
without_tracking_correction=True

def process_experiment(experiment):
    data_dir = os.path.abspath(os.path.join(processing_dir, experiment, 'CP_output'))
    cp_csv = os.path.join(data_dir, 'tracking_cells.csv') # Use the newer format method # Path to cellprofiler data output
    npy_dir = os.path.join(data_dir, 'omnipose_images') # Path to .npy file directory from Omnipose output
    neighbour_csv = os.path.join(data_dir, 'tracking_Object relationships.csv') # Path to cellprofiler neighbour output
    
    print(f"Processing experiment {experiment}")
    process_data(input_file=cp_csv, npy_files_dir=npy_dir, neighbors_file=neighbour_csv,
                     output_directory=output_directory, interval_time=dt, growth_rate_method=growth_rate_method,
                     number_of_gap=0, um_per_pixel=0.144, intensity_threshold=0.1,
                     assigning_cell_type=assigning_cell_type, min_life_history_of_bacteria=min_life_history_of_bacteria, 
                     warn=warn, without_tracking_correction=without_tracking_correction)

    # Write to log file
    output_to_log_file(experiment)

def output_to_log_file(experiment, log_file_name='TrackRefiner_processing_log.txt'):
    # Append-adds at last
    file1 = open(log_file_name, "a")  # append mode
    output = f'Finished processing {experiment} \n'
    file1.write(output)
    file1.close()

if __name__ == '__main__':
    # Get list of experiments to process
    experiments = os.listdir(processing_dir)
    
    # Process experiments in parallel
    with ProcessPoolExecutor(max_workers=6) as executor:
        executor.map(process_experiment, experiments)