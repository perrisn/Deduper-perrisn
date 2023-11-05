#!/bin/bash

#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=bgmp             #REQUIRED: which partition to use
#SBATCH --mail-user=perrisn@uoregon.edu     #optional: if you'd like email
#SBATCH --mail-type=ALL                   #optional: must set email first, what type of email you want
#SBATCH --cpus-per-task=1                 #optional: number of cpus, default is 1
#SBATCH --mem=8GB                        #optional: amount of memory, default is 4GB

conda activate samtools
samtools sort /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam -o C1_SE_uniqAlign.sam
conda deactivate

conda activate base
/usr/bin/time -v ./Navarro_deduper.py -f /projects/bgmp/perrisn/bioinfo/Bi624/sorted_sam.sam \
-o /projects/bgmp/perrisn/bioinfo/Bi624/output_file.sam -u /projects/bgmp/perrisn/bioinfo/Bi624/Deduper-perrisn/STL96.txt