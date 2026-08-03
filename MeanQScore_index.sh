#!/bin/bash      
#SBATCH --account=bgmp                    # REQUIRED: which account to use
#SBATCH --partition=bgmp                  # REQUIRED: which partition to use
#SBATCH --cpus-per-task=8                 # optional: number of cpus, default is 1
#SBATCH --mem=16GB                        # optional: amount of memory, default is 4GB per cpu
#SBATCH --job-name=R3                     # optional: job name

DATA=/projects/bgmp/shared/2017_sequencing
R2=$DATA/1294_S1_L008_R2_001.fastq.gz
R3=$DATA/1294_S1_L008_R3_001.fastq.gz

# /usr/bin/time -v python MeanQScore_index.py -f $R2 -r R2
/usr/bin/time -v python MeanQScore_index.py -f $R3 -r R3


