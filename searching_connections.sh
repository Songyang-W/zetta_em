#!/bin/bash -l
#this makes it so you'll get an email at the (b)eginning of the job, (e)nd of the job, and on an (a)bort of the job
#$ -m ea
#this merges output and error files into one file
#$ -j y
#this sets the project for the script to be run under
#$ -P jchenlab
#Specify the time limit
#$ -l h_rt=2:00:00
#$ -pe omp 8
#$ -l mem_per_core=3G

module load miniconda
mamba activate em_skeleton
python axon_dend_close_nodes_logrealtime.py
