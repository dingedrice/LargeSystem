#!/bin/bash

# Define the Slurm arguments in a clean list
sbatch_opts=(
    --parsable
    --job-name="npc"
	--time=23:59:00 
	--ntasks=1 
	--cpus-per-task=4 
	--threads-per-core=1 
	--mem-per-cpu=8GB 
	--gres=gpu:1 
	--export=ALL
)

for i in {1..20}
do
	if ((i < 11))
	then
		PARTITION="ctbp-onuchic"
	else
		PARTITION="ctbp-common"
	fi
	cmd="module purge; \
		export XALT_EXECUTABLE_TRACKING=no; \
		unset LD_PRELOAD; \
		srun singularity exec --nv \
		/opt/apps/examples/OpenMM/ctbp-environment-05132025.sif \
		python run.py $i"

	FIRST_JOB_ID=$(sbatch "${sbatch_opts[@]}" --account=$PARTITION --partition=$PARTITION --wrap="$cmd")
	SECOND_JOB_ID=$(sbatch --dependency=afterany:$FIRST_JOB_ID "${sbatch_opts[@]}" --account=$PARTITION --partition=$PARTITION --wrap="$cmd")
done
