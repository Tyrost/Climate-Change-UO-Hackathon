#!/bin/bash
#SBATCH --partition=gpu           ### Partition (like a queue in PBS)
#SBATCH --job-name=CARBS_ML        ### Job Name
#SBATCH --output=slurm_logs/%x.%j.out ### File in which to store job output
#SBATCH --error=slurm_logs/%x.%j.err  ### File in which to store job error messages
#SBATCH --time=0-10:00:00          ### Wall clock time limit in Days-HH:MM:SS 
#SBATCH --gpus=1                   ### Number of GPUs needed
#SBATCH --constraint=gpu-80gb      ### Constraint to use 80GB GPUs
#SBATCH --ntasks-per-node=1        ### Number of tasks to be launched per Node
#SBATCH --account=datascience      ### Account used for job submission
#SBATCH --cpus-per-task=4         ### Number of CPUs per task
#SBATCH --mem=200G                 ### Memory required
#SBATCH --nodes=1                  ### Node count required for the job
#SBATCH --gres=gpu:1  ### Request 1 GPU with 80GB memory

python train.py
