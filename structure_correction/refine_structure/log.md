Take `dilated` as an example
1. Generate `d${i}.pdb` from vmd with `sub.pdb`.
2. `./seq.sh` to generate `d${i}_input.pdb`. The sequence information is added for the requirement of the pdbfixer package.
3. remove residues that needs to be refined in `d${i}_input.pdb`.
4. `python refine.py`.
5. `python rotate.py` because `d7.pdb` is from the second subunit.
6. copy the fixed files into `d${i}_fixed_final.pdb` and adjust the order of some atoms.
7. `cp /mnt/e/LargeSystem/npc/original_structure/dilated/sub1_TER.pdb dilated_final.pdb`, and modify this file based on fixed d${i}.
