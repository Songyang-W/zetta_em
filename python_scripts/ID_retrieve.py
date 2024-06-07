import csv
import sys
import os
import numpy as np
from cloudvolume import CloudVolume
from glob import glob 
import fastremap
import pickle 
from scipy.io import savemat

def pull_out_ID(line,cv,ID_cell,vol_size,save_dir):
     # input should be [x,y,z]
     ID_xyz = line.split(',')
     x_start = max(0, int(ID_xyz[0])-vol_size)
     x_end = min(25000,int(ID_xyz[0])+vol_size)
     y_start = max(0, int(ID_xyz[1])-vol_size)
     y_end = min(22000,int(ID_xyz[1])+vol_size)
     z_value = int(ID_xyz[2])
     if z_value < 1344 or z_value > 3748:
          print(f"z-value {z_value} is out of the allowable range (1344 to 3748). Exiting function.")
          return
     z_start = max(1344, int(ID_xyz[2])-5)
     z_end = min(3748, int(ID_xyz[2])+5)
     vol = cv[x_start:(x_start+vol_size*2),y_start:(y_start+vol_size*2),z_start:z_end]
     new_vol = np.squeeze(vol, axis=-1)
     ptc = fastremap.point_cloud(new_vol)
     csv_path = f"{save_dir}.csv"
     with open(csv_path, 'a', newline='') as file:
          writer = csv.writer(file)
          for ID, roi in ptc.items():
              writer.writerow([str(ID)])  # Write ID as int



vol_size = 500

cv = CloudVolume('gs://zetta_jchen_mouse_cortex_001_segmentation/nuclei/rough_aligned/seg_v1', parallel=True, progress=True)
csv_files = glob("/net/claustrum3/mnt/data/Projects/Connectomics/Animals/jc105/EM_volume/missing_rois/*")

for csv_file in csv_files:
    # Extract the name of the CSV file without extension
    csv_name = os.path.splitext(os.path.basename(csv_file))[0]
    
    # Set the save directory based on the CSV file name
    save_dir = f'/net/claustrum3/mnt/data/Projects/Connectomics/Animals/jc105/EM_volume/mat_files/june_4_missing/{csv_name}'
    
    # Create the directory if it does not exist
    ID_cell = {}
    expected_csv_path = f"{save_dir}.csv"
    if os.path.exists(expected_csv_path):
        print(f"File {expected_csv_path} already exists, skipping.")
        continue

    with open(csv_file, 'r') as f:
        for line in f:
            pull_out_ID(line, cv, ID_cell, vol_size, save_dir)
