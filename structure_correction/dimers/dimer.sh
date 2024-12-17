#!/bin/bash

# Generate a dimer from the monomer in refine_structure/
python dimer.py

# Convert dimer structure from PDB to GRO
echo 0 | gmx trjconv -f dilated_dimer.pdb -s /mnt/e/LargeSystem/npc/original_structure/dilated/original_SBM/openmm_del/dilated.gro -o dilated_dimer.gro
echo 0 | gmx trjconv -f constricted_dimer.pdb -s /mnt/e/LargeSystem/npc/original_structure/constricted/original_SBM/openmm_del/constricted.gro -o constricted_dimer.gro

# Change the box size at the last line
sed -i "$ d" dilated_dimer.gro 
echo "200.00000   200.00000   200.00000" >> dilated_dimer.gro
sed -i "$ d" constricted_dimer.gro 
echo "200.00000   200.00000   200.00000" >> constricted_dimer.gro
