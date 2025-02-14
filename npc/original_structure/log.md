Take `dilated` as an example
1. Download the CIF file 7r5j-assembly1.cif.gz and run `gzip -d 7r5j-assembly1.cif.gz`
2. Use vmd to extract the first and second subunits and generate `sub1.pdb` and `sub2.pdb`
3. Run the following code `python ../add_TER.py sub1.pdb sub1_TER.pdb`, `python ../add_TER.py sub2.pdb sub2_TER.pdb`, `cat sub1_TER.pdb sub2_TER.pdb > sub.pdb`. The first `END` in `sub.pdb` was changed to `TER` and the tile of the second part was removed. This combines the two subunits.
PS: The PDB bundles are obtained from PDB bank and tested. They give the same results.
4. The SBM was generated on the Aries cluster

5. The adjust_1.pdb was generated from smog_adjustPDB for subunit 1 as a template for future use.
