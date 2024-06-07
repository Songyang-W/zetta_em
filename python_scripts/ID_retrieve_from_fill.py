import csv
import sys
import os
import numpy as np
from cloudvolume import CloudVolume
from glob import glob 
import fastremap
import pickle 
from scipy.io import savemat

def extract_data_from_array(array, csv_file_path):
    extracted_data_list = []
    results = []
    
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert string indices to integer
            indices = list(map(int, row))
            # Check if the last index is smaller than 1344
            if indices[-1] < 1344 or indices[-1] > 3747:
                extracted_data = 0
            else:
                # Extract data using indices and simplify the structure
                extracted_data = array[tuple(indices)].item()  # Use .item() to get Python scalar
                
            extracted_data_list.append(extracted_data)  # Append the simplified extracted data
            results.append((indices, extracted_data))  # Append tuple to results list
            
            print(f"Indices: {indices} -> Data: {extracted_data}")

    results_array = np.array(results, dtype=object)  # Convert results list to a NumPy array for structured results
    return extracted_data_list, results_array


cv = CloudVolume('gs://zetta_jchen_mouse_cortex_001_segmentation/nuclei/rough_aligned/seg_v1', parallel=True, progress=True)
csv_file_path = '/net/claustrum3/mnt/data/Projects/Connectomics/Animals/jc105/EM_volume/coordinates.csv'
# Example usage:
extracted_data, results = extract_data_from_array(cv, csv_file_path)
# print("Extracted Data List:", extracted_data)
# print("Results Array:", results)

flattened_data = [item[0] + [item[1]] for item in results]
data = np.array(flattened_data, dtype=np.int64)
savemat('coordinatesXYZ_filled_w_ID_redo.mat', {'coordinates': data})
print(np.unique(extracted_data))
