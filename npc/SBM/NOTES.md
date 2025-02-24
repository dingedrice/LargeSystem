1. The structure after energy minimization was analyzed in the folder `../emin/` and the octamers for constricted and dilated structure were generated.
2. The octamers were used to generate the AA and CA SBM on the aries cluster, stored in folder `constricted` and `dilated` under this folder.
3. There are multiple large native angles (greater than 150) in the CA model. They may lead to linear conformations which cause problem for dihedral calculations. Thus, the dihedral terms related to these angles were removed from the CA model using `xml.ipynb`.
