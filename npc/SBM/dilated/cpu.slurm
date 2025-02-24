#!/bin/bash -l

#SBATCH --job-name=openmm
#SBATCH --account=highmem
#SBATCH --partition=highmem
#SBATCH --ntasks=1
#SBATCH --time=06:00:00
#SBATCH --mem-per-cpu=32G
#SBATCH --cpus-per-task=1
#SBATCH --threads-per-core=1

conda deactivate
container=/home/pcw2/bin/SMOGgit-OpenSMOGgit-MiChroM-MDtraj-Nov2024.sif
singularity exec $container smog2 -i dilated_reconstruct.pdb -dname dilated_AA -OpenSMOG -limitcontactlength -t /home/ed31/SBM_AA-amber-bonds/
singularity exec $container smog2 -i dilated_reconstruct.pdb -dname dilated_CA -OpenSMOG -limitcontactlength -CA
