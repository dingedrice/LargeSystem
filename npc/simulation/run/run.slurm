#!/bin/bash -l
#SBATCH -J run_init
#SBATCH -o job.%j.out
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -p mi2104x
#SBATCH --time=23:59:00

container=/home1/george/SMOGgit-OpenSMOGgit-MiChroM-MDtraj-Nov2024.sif

# Run 1
NAME=d; GPU=0; INDEX=1; mkdir ${NAME}_${INDEX}; singularity exec $container python3 run.py $NAME $GPU $INDEX &> ${NAME}_${INDEX}/output.log &

# Run 2
NAME=d; GPU=1; INDEX=2; mkdir ${NAME}_${INDEX}; singularity exec $container python3 run.py $NAME $GPU $INDEX &> ${NAME}_${INDEX}/output.log &

# Run 3
NAME=c; GPU=2; INDEX=1; mkdir ${NAME}_${INDEX}; singularity exec $container python3 run.py $NAME $GPU $INDEX &> ${NAME}_${INDEX}/output.log &

# Run 4
NAME=c; GPU=3; INDEX=2; mkdir ${NAME}_${INDEX}; singularity exec $container python3 run.py $NAME $GPU $INDEX &> ${NAME}_${INDEX}/output.log &

# this is important, to ensure the jobs all complete before the script exits.
wait
