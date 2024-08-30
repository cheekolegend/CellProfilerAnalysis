import os
import subprocess
from pathlib import Path
from Trackrefiner.strain.processCellProfilerData import process_data
import pandas as pd

os.environ['PYTHONBREAKPOINT'] = '0' # Disable breakpoints

win_path = r'C:\Users\aaron\OneDrive - University of Waterloo\Research\Papers\Conjugation_paper\conjugation_detection_validation\scene2_CPoutput' # Path to folder containing all data
win_path = r'C:\Users\aaron\OneDrive\Documents\ilastik_cp_run\run\scene1\CP_output'
data_dir = Path(win_path)

cp_csv = os.path.join(data_dir, 'tracking_cells_tiny.csv') # Use the newer format method # Path to cellprofiler data output
npy_dir = os.path.join(data_dir, 'omnipose_images_tiny') # Path to .npy file directory from Omnipose output
neighbour_csv = os.path.join(data_dir, 'tracking_Object relationships_tiny.csv') # Path to cellprofiler neighbour output
output_directory = None # None defaults to output in same directory as tracking csv file
dt = 5/60 # h
min_life_history_of_bacteria = 5/60
growth_rate_method = "Linear Regression"
assigning_cell_type = False
warn = True
without_tracking_correction=False
boundary_limit = None
clf = 'LogisticRegression'
n_cpu = -1 # -1 means use all available

df = pd.read_csv(cp_csv)
print(df)


process_data(input_file=cp_csv, npy_files_dir=npy_dir, neighbors_file=neighbour_csv,
                 output_directory=output_directory, interval_time=dt, growth_rate_method=growth_rate_method,
                 number_of_gap=0, um_per_pixel=0.144, intensity_threshold=0.1,
                 assigning_cell_type=assigning_cell_type, min_life_history_of_bacteria=min_life_history_of_bacteria, 
                 warn=warn, without_tracking_correction=without_tracking_correction, clf=clf, n_cpu=n_cpu,
                 boundary_limits=boundary_limit)

'''
if __name__ == '__main__':
    # Run TrackRefiner
    command = [
    'python runPostProcessing',
    '-i', f'{cp_csv}',
    #'-np', f'{npy_dir}',
    #'-r', f'{neighbour_csv}',
    '-it', f'{dt}',
    '-m', f'{minLifeHistory}',
    '-g', f'{growth_rate_method}',
    '-a', f'{cellType}'
    ]
    print("  ".join(command))
    subprocess.run(command, check=True)
'''