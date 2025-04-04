#!/bin/bash -l
#this makes it so you'll get an email at the (b)eginning of the job, (e)nd of the job, and on an (a)bort of the job
#$ -m ea
#this merges output and error files into one file
#$ -j y
#this sets the project for the script to be run under
#$ -P jchenlab
#Specify the time limit
#$ -l h_rt=1:00:00
#$ -pe omp 8
#$ -l mem_per_core=3G


cd /projectnb/jchenlab/lab-soft/
module use /projectnb/jchenlab/lab-soft/module.8/bioinformatics
module load python3/3.10.12
module load google-cloud-sdk/455.0.0
module load tensorflow/2.11.0
module load segclr/2024-10-25_git64b309c
source $SCC_SEGCLR_DIR/connect_venv/bin/activate
cd /projectnb/jchenlab/Projects/Connectomics/EM/

python preprocess_volume_60nm.py

chmod -R 777 /projectnb/jchenlab/Projects/Connectomics/EM/
