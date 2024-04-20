#!/bin/bash


#SBATCH --job-name=python_video_query        # Job name
#SBATCH --output=python_video_job_%j.out     # Output file. %j will be replaced with the job ID
#SBATCH --cpus-per-task=4                    # Number of CPU cores per task
#SBATCH --mem=16gb                           # Memory total in MB (for all cores)
#SBATCH --time=36:00:00                      # Time limit hrs:min:sec
#SBATCH --partition=brown                    # Run on either the Red or Brown queue
#SBATCH --mail-type=BEGIN,FAIL,END           # Mail events (NONE, BEGIN, END, FAIL)
#SBATCH --mail-user=youremail@domain.com     # Email to send the mail events


# File path should be: ./src/pagerankings_outputs/.....


python3 ./src/video_query.py key secret file_path