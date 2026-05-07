# Pipeline
1. `original_structure` 

    Generate original SBM.

2. `get_faulty_bonds`

    Refine the structure with energy minimization to generate a symmetric unit. Then generate the new SBM. This SBM contains problematic bonds, implying that we needs further correction of the original structure.

3. `structure_correction`

    Correct the original structure by repositioning the atoms associated with the problematic bonds. e.g. take the bond out of the ring (this is likely a mistake from there structure refinement tools).

4. `emin`

    Refine the structure with energy minimization to generate a symmetric unit. The strategy is similar to step 2.

5. `SBM`

    Generate the new SBM. The strategy is similar to step 2. The SBM generated in this step is the final SBM for the simulations.

6. `simulation`

    Run the simulations with the final SBM. 