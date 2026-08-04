#!/bin/bash

# Define the Slurm arguments in a clean list
sbatch_opts=(
    --parsable
    --job-name="npc"
	--account=commons
	--partition=commons
	--time=23:59:00 
	--ntasks=1 
	--cpus-per-task=4 
	--threads-per-core=1 
	--mem-per-cpu=8GB 
	--gres=gpu:lovelace:1 
	--export=ALL
)

for i in {1..20}
do
	cmd="module purge; \
		export XALT_EXECUTABLE_TRACKING=no; \
		unset LD_PRELOAD; \
		srun singularity exec --nv \
		/opt/apps/examples/OpenMM/ctbp-environment-05132025.sif \
		python run.py $i"

	sbatch "${sbatch_opts[@]}" --wrap="$cmd"

done
