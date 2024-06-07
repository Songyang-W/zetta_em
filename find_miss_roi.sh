#!/bin/bash -l
#this makes it so you'll get an email at the (b)eginning of the job, (e)nd of the job, and on an (a)bort of the job
#$ -m ea
#this merges output and error files into one file
#$ -j y
#this sets the project for the script to be run under
#$ -P jchenlab
#$ -e log_files/find_miss_roi.sh.error
#Specify the time limit
#$ -l h_rt=4:00:00
#$ -pe omp 4
#$ -l mem_per_core=1G


module load python3/3.10.12
source /projectnb/jchenlab/venvs/zetta_em/bin/activate 

cd /net/claustrum3/mnt/data/Projects/Connectomics/Animals/jc105/EM_volume

python ID_retrieve.py
