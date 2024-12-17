#!/bin/bash

dos2unix d*.pdb;
for i in `seq 7`;
do
	python ../SEQRES.py d${i}.pdb seq${i};
	cat seq${i} d${i}.pdb > d${i}_input.pdb;
done
# The d${i}_input.pdb files were then modified by hand to remove some atoms
