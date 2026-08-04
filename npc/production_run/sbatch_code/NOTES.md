This folder contians example code to submit the simulation on NOTS, either with the commons, ctbp-common, or ctbp-onuchic partition. THe commons partition is about twice as fast as the other two. 

The `sbatch_commons.sh` file submit jobs on the commons partition, and the `sbatch_ctbp.sh` submit two consecutive jobs on either ctbp-common or ctbp-onuchic

`run.py` contains the python code to run the simulation or the original model ($H_0$)