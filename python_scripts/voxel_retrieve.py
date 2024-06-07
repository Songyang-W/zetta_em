import sys
import numpy as np
from cloudvolume import CloudVolume
from glob import glob 
import fastremap
import pickle 
from scipy.io import savemat

def pull_out_voxel(line,cv,existing_dict,vol_size):
     ID_xyz = line.split(',')
     ID = int(ID_xyz[0])
     x_start = max(0, int(ID_xyz[1])-vol_size)
     x_end = min(25000,int(ID_xyz[1])+vol_size)
     y_start = max(0, int(ID_xyz[2])-vol_size)
     y_end = min(22000,int(ID_xyz[2])+vol_size)
     z_start = max(1344, int(ID_xyz[3])-vol_size)
     z_end = min(3748, int(ID_xyz[3])+vol_size)
     voxel_size =  int(ID_xyz[4])
     vol = cv[x_start:(x_start+vol_size*2),y_start:(y_start+vol_size*2),z_start:z_end]
     new_vol = np.squeeze(vol, axis=-1)
     ptc = fastremap.point_cloud(new_vol)
     roi = ptc[ID]
     roi_adjusted = roi + np.array([x_start,y_start,z_start])
     roi_uint16 = roi_adjusted.astype(np.uint16)
     existing_dict[ID] = roi_uint16
     print('done one line')
     return ID,roi_uint16

save_dir = '/net/claustrum3/mnt/data/Projects/Connectomics/Animals/jc105/EM_volume/mat_files/june7_97/'
vol_size = 500
merged_dict = {}
cv = CloudVolume('gs://zetta_jchen_mouse_cortex_001_segmentation/nuclei/rough_aligned/seg_v1', parallel=True, progress=True)
with open('output_0607.csv', 'r') as f:
    for line in f:
         ID,roi = pull_out_voxel(line,cv,merged_dict,vol_size)
         filename = save_dir + str(ID)+'.mat'
         formatted_data = {'roi':roi}
         savemat(filename, formatted_data)

