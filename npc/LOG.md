# Pipeline
1. `original_structure` 

    Generate original SBM.

2. `get_faulty_bonds`

    Refine the structure with energy minimization to generate a symmetric unit. Then generate the new SBM. This SBM contains problematic bonds, implying that we needs further correction of the original structure.

3. `structure_correction`

    Correct the original structure by repositioning the atoms associated with the problematic bonds. e.g. take the bond out of the ring (this is likely a mistake from there structure refinement tools).

4. `emin`

    Refine the structure with energy minimization to generate a symmetric unit. The strategy is similar to step 2.
    P.S. The refined structures are stored under npc/ instead of npc/emin in this repo.

5. `SBM`

    Generate the new SBM. The strategy is similar to step 2. The SBM generated in this step is the final SBM for the simulations.

6. `simulation`

    Benchmark the system with the final SBM, run the equilibration simulations and extract the conformations for the downhill simulations.

7. `production_run`

    Downhill simulations for the project.
