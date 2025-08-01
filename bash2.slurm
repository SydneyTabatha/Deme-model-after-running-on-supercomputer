#!/bin/bash
#SBATCH --job-name=replicate_job
#SBATCH --output=slurm_output_%A_%a.out
#SBATCH --error=slurm_error_%A_%a.err
#SBATCH --array=1-1024
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

# Create a unique output file for this job
OUTPUT_FILE="m${SLURM_ARRAY_TASK_ID}.dat"

# Optional small stagger to reduce cluster overload
sleep $(echo "${SLURM_ARRAY_TASK_ID} * 0.01" | bc -l)

# Call the Python script
python3 multi_patch_july_11.py ${OUTPUT_FILE}
