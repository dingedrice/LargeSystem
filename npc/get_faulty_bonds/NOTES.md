NOTE: some files are already lost but the strategy is the same as in folder `emin`

1. After obtaining the original SBM, energy minimization was carried out in order to refine the interfaces and get the structure of one symmetrical unit. Just as in the folder `emin`. 
2. After generating the SBM for this symmetrical unit, there remain faulty bonds because of the unphysical local structures. The faulty structures are extracted from the error message of the SMOG2 output for SBM and later corrected in the folder `structure_correction`.
The faulty bonds are included in `bond_constricted` and `bond_dilated`
