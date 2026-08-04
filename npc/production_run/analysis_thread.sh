#!/bin/bash

# Submit analysis script for the NPC systems on oldnots with CPU
# Define the Slurm arguments in a clean list
sbatch_opts=(
    --parsable
    --job-name="ana"
	--account=ctbp-common 
	--partition=ctbp-common 
	--time=23:50:00 
	--ntasks=1 
	--cpus-per-task=1 
	--threads-per-core=1 
	--mem-per-cpu=16GB 
)

for i in */
do
	for j in {1..20}
	do
		dir=$i/$j
		input_j=$(( (j+1)/2 ))
		if [[ -d $dir ]]
		then
			cmd="python /home/ed31/npc_scripts/trj_ana_tool.py $dir /scratch-new/ed31/npc_run/simulation/d${input_j}_input.gro"
			JOB=$(sbatch "${sbatch_opts[@]}" --wrap="$cmd")
		fi 
	done
done
