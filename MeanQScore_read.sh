#!/bin/bash      
#SBATCH --account=bgmp                    # REQUIRED: which account to use
#SBATCH --partition=bgmp                  # REQUIRED: which partition to use
#SBATCH --cpus-per-task=8                 # optional: number of cpus, default is 1
#SBATCH --mem=16GB                        # optional: amount of memory, default is 4GB per cpu
#SBATCH --job-name=R4                     # optional: job name

DATA=/projects/bgmp/shared/2017_sequencing
R1=$DATA/1294_S1_L008_R1_001.fastq.gz
R4=$DATA/1294_S1_L008_R4_001.fastq.gz

# /usr/bin/time -v python MeanQScore_read.py -f $R1 -r R1 
/usr/bin/time -v python MeanQScore_read.py -f $R4 -r R4

