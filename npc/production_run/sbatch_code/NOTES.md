1. This folder contians example code to submit the simulation on NOTS, either with the commons, ctbp-common, or ctbp-onuchic partition. THe commons partition is about twice as fast as the other two. 

2. The `sbatch_commons.sh` file submit jobs on the commons partition, and the `sbatch_ctbp.sh` submit two consecutive jobs on either ctbp-common or ctbp-onuchic

3. `run.py` contains the python code to run the simulation or the original model ($H_0$)

4. Six folders originally exist under `production_run` with six different Hamiltonians: `production_run/d2c` ($H_0$), `production_run/intrachain_linker` ($H_1$), `production_run/intrachain_irnonlinker` ($H_2$), `production_run/interchain_linker` ($H_3$), `production_run/IRinterface_weaken` ($H_4$), and `production_run/bridge_dualbasin` (agnostic Bridges)
