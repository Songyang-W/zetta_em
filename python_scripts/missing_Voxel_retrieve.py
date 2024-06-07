import sys
import os
import numpy as np
from cloudvolume import CloudVolume
from glob import glob 
import fastremap
import pickle 
from scipy.io import savemat

def pull_out_voxel(line,cv,existing_dict,vol_size,save_dir):
     # input should be [x,y,z]
     ID_xyz = line.split(',')
     x_start = max(0, int(ID_xyz[0])-vol_size)
     x_end = min(25000,int(ID_xyz[0])+vol_size)
     y_start = max(0, int(ID_xyz[1])-vol_size)
     y_end = min(22000,int(ID_xyz[1])+vol_size)
     z_start = max(1344, int(ID_xyz[2])-vol_size)
     z_end = min(3748, int(ID_xyz[2])+vol_size)
     vol = cv[x_start:(x_start+vol_size*2),y_start:(y_start+vol_size*2),z_start:z_end]
     new_vol = np.squeeze(vol, axis=-1)
     ptc = fastremap.point_cloud(new_vol)
     for ID, roi in ptc.items():
          roi_adjusted = roi + np.array([x_start,y_start,z_start])
          roi_uint16 = roi_adjusted.astype(np.uint16)
          if ID in existing_dict:
               combined_rois = np.vstack((existing_dict[ID], roi_uint16))
               unique_rois = np.unique(combined_rois, axis=0)
               existing_dict[ID] = unique_rois
          else:
               existing_dict[ID] = roi_uint16
     for ID,roi in existing_dict.items():
          filename = save_dir + str(ID)+'.mat'
          formatted_data = {'roi':roi}
          savemat(filename, formatted_data)



vol_size = 500

cv = CloudVolume('gs://zetta_jchen_mouse_cortex_001_segmentation/nuclei/rough_aligned/seg_v1', parallel=True, progress=True)
csv_files = glob("/net/claustrum3/mnt/data/Projects/Connectomics/Animals/jc105/EM_volume/missing_rois/*")

for csv_file in csv_files:
    # Extract the name of the CSV file without extension
    csv_name = os.path.splitext(os.path.basename(csv_file))[0]
    
    # Set the save directory based on the CSV file name
    save_dir = f'/net/claustrum3/mnt/data/Projects/Connectomics/Animals/jc105/EM_volume/mat_files/june_4_missing/{csv_name}/'
    
    # Create the directory if it does not exist
    os.makedirs(save_dir, exist_ok=True)
    merged_dict = {}
    with open(csv_file, 'r') as f:
        for line in f:
            pull_out_voxel(line, cv, merged_dict, vol_size, save_dir)
