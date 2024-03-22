#!/bin/bash


#SBATCH --job-name=python_network_query    # Job name
#SBATCH --output=python_job_%j.out         # Output file. %j will be replaced with the job ID
#SBATCH --cpus-per-task=4                  # Number of CPU cores per task
#SBATCH --mem=4gb                          # Memory total in MB (for all cores)
#SBATCH --time=02:00:00                    # Time limit hrs:min:sec
#SBATCH --partition=brown                  # Run on either the Red or Brown queue
#SBATCH --mail-type=FAIL,END,BEGIN         # Mail events (NONE, BEGIN, END, FAIL, ALL)

# Load any modules or software you need
# module load python3

# Execute the Python script
python3 src/main.py