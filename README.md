# Using the code on BU SCC

## Instructions:

1. ``qsub ID_retrieving_from_fill.sh``

Function of the code is to pullout the ID from a given xyz coordinate, 0 if no ID related.

the line will activate the cloudvolume package
``source /projectnb/jchenlab/venvs/zetta_em/bin/activate ``

``ID_retrieve_from_fill.py`` is the key python code under this directory: ``/net/claustrum3/mnt/data/Projects/Connectomics/Animals/jc105/EM_volume ``
the expected input for ``ID_retrieve_from_fill.py`` is a column of x,y,z coordinate (see sample data: ``coordinate.csv``).
There will be two outputs: one matfile with size of nx4 matrix, one printed array of unique ID in the output file (ID_retrieving_from_fill.sh.o**)

2. pullout_mat.sh

function of the code is to pull out the voxel coordinates of a given ID, centroids

``voxel_retrieve.py`` is the key python code (same above)

the expected input is ID,X,Y,Z,M (subset of main_em_soma.csv)

output is mat file with ID as filename, and coordinates as content


## Notes

Zetta provides us with ``240516-jchen-s1-rough-nuclei-v1-60-60-50.csv`` file which contains the soma ID (17 numbers) and centroids (x,y,z) and voxel size (m)

the cloud volume directory: 
``gs://zetta_jchen_mouse_cortex_001_segmentation/nuclei/rough_aligned/seg_v1', parallel=True``
(get the code to extract the ROI below)

Jerry would give me the ID and ask me to pull out all the coordinates for the voxel. Zetta has a written function to do so

Because Jerry used excel and matlab to process the ‘240516-jchen-s1-rough-nuclei-v1-60-60-50.csv’ which didn’t load 17 numbers correctly (round to 15 or 16 numbers — need to find the best way load the csv file). I wrote a matlab code to find the line number, and use line number to pull out the id+coordinates from the main.csv

this can be helpful
``readmatrix("240516-jchen-s1-rough-nuclei-v1-60-60-50.csv",'OutputType','int64');``

pull out voxel coordinates from cloudvolume is not hard. Zetta written function could do it. Basic idea is to extract 1000x1000x1000 volume according to the center, and find the id

the code has been saved 

SCC:
``/net/claustrum3/mnt/data/Projects/Connectomics/Animals/jc105/EM_volume/voxel_retrieve.py
~/repo/zetta_em/pullout_mat.sh``

O2:
``/n/data3/hms/neurobio/htem/temcagt/datasets/jc105_r214/sections/python_codes/voxel_retriev_test.py``

June 4
jerry found 80 neurons I identified in 2P but not co-registered in EM, to find the possible EM, I first use the coordinate Jerry gave me (he transferred the coordinate from 2P to EM, ask him How, so I can know the +-)
Then, I use the same method, to extract 1000x1000x1000 volume to extract all ROI:Coordinate file, and save them into a folder. Hopefully, jerry can load them all into neurotator
- [x] try to do a stats on which EM soma is the one we need — for each z-slide, I can pull out a list of ROIs, and from that ROI list, I want to see if any of it showed up really frequent

Jerry only wants me to give him one output (ID/0) from each coordinate he provided.


