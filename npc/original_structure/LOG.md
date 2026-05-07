Take `dilated` as an example

1. Download the CIF file 7r5j-assembly1.cif.gz and run `gzip -d 7r5j-assembly1.cif.gz` in the newly created folder `dilated`.

2. Use vmd to extract the first and second subunits and generate `sub1.pdb` and `sub2.pdb` in the folder `dilted`.

3. Run the following code in the folder `dilated`: `python ../add_TER.py sub1.pdb sub1_TER.pdb`, `python ../add_TER.py sub2.pdb sub2_TER.pdb`, `cat sub1_TER.pdb sub2_TER.pdb > sub.pdb`. The first `END` in `sub.pdb` was changed to `TER` and the title of the second part was removed. This combines the two subunits and generate the file `sub.pdb`.

PS: The PDB bundles are obtained from PDB bank and tested. They give the same results.

4. The SBM was generated on the Aries cluster as follows, and the results are included in the folder `original_SBM` inside `dilated`. First, generate `adjusted.pdb` using `smog_adjustPDB -i ../sub.pdb -map /mnt/e/LargeSystem/SBM_AA-amber-bonds/map.SBM_AA-amber-bonds`. Then, create a folder named `openmm_del` in `original_SBM`, and run the following command on the cluster inside `original_SBM/openmm_del`: `smog2 -i ../adjusted.pdb -dname constricted -OpenSMOG -deleteshortcontact -t /home/ed31/SBM_AA-amber-bonds/`.

5. The adjust_1.pdb was generated from smog_adjustPDB for subunit 1 as a template for future use.
