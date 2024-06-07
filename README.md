**Using the code on BU SCC**

Instructions:

``qsub ID_retrieving_from_fill.sh``

Function of the code is to pullout the ID from a given xyz coordinate, 0 if no ID related.

the line will activate the cloudvolume package
``source /projectnb/jchenlab/venvs/zetta_em/bin/activate ``

``ID_retrieve_from_fill.py`` is the key python code under this directory: ``/net/claustrum3/mnt/data/Projects/Connectomics/Animals/jc105/EM_volume ``
the expected input for ``ID_retrieve_from_fill.py`` is a column of x,y,z coordinate (see sample data: ``coordinate.csv``).
There will be two outputs: one matfile with size of nx4 matrix, one printed array of unique ID in the output file (ID_retrieving_from_fill.sh.o**)
