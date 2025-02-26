Take `dilated` as an example
1. Generate `d${i}.pdb` from vmd with `sub.pdb`.
2. Use `structure.ipynb` to refine the loop, rearange the atoms to match the order, and sometimes rotate the residues from the second subunit to the first. 
3. `cp /mnt/e/LargeSystem/npc/original_structure/dilated/sub1_TER.pdb dilated_final.pdb`, and modify this file based on `d${i}_fixed.pdb`.

NOTE: The function `reorganize_pdb` can be rewritten to be faster. the Jupyter notebooks are not changed and the new function is attached in `reorganize_pdb.py` without further tests.
