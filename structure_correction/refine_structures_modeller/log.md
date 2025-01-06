Take `dilated` as an example
1. Generate `d${i}.pdb` from vmd with `sub.pdb`.
2. Use `structure.pdb` to refine the loop, rearange the atoms to match the order, and sometimes rotate the residues from the second subunit to the first. 
7. `cp /mnt/e/LargeSystem/npc/original_structure/dilated/sub1_TER.pdb dilated_final.pdb`, and modify this file based on `d${i}_fixed.pdb`.
