# Calculate the RMSD of the linker regions, with the last 20 residues of Nup35 removed.
import sys
import os
sys.path.append('/home/ed31/npc_scripts')
from npc_ana_tool import *

import MDAnalysis as mda
from MDAnalysis.analysis import rms, align
from MDAnalysis.lib.distances import calc_bonds

work_dir = '/home/ed31/npc_template'

# import mdtraj as md
reffile=f'{work_dir}/constricted_CA.pdb'
ref = mda.Universe(reffile)

sim_dic = sys.argv[1]
sim_init = sys.argv[2]
seq_all = [f"_{i}" for i in range(1, 11)] + [""]
dcd_path = [sim_init] # Start with the initial structure

for seq in seq_all:
    oldfile = f"{sim_dic}/npc_trajectory.dcd{seq}"
    newfile = f"{sim_dic}/npc_trajectory{seq}.dcd"
    try:
        os.rename(oldfile, newfile)
    except FileNotFoundError:
        pass
    if os.path.isfile(newfile):
        dcd_path.append(newfile)

trj = mda.Universe(reffile, dcd_path) 

# Remove the end helix as it is flexible
id_linkers = []
for start, end in zip(df_chain_info.query('Nup == "Nup35"')['CA_start'], df_chain_info.query('Nup == "Nup35"')['CA_end'] - 20):
    tmp_list = [np.arange(start, end+1) + k*N_subunit_CA for k in range(Nsubunits)]
    id_linkers.append(np.array(tmp_list))


rmsd_chains_all_frames = []
for ts in trj.trajectory:
    # indicate progress
    if ts.frame % 100 == 0:
        print(f"Processing frame {ts.frame}/{len(trj.trajectory)}")
    rmsd_chains = []
    for id_nup in id_linkers:
        rmsd_nup = []
        for chain in id_nup:
            ag_u = trj.atoms[chain]
            ag_ref = ref.atoms[chain]
            val = rms.rmsd(ag_u.positions, ag_ref.positions, superposition=True)
            rmsd_nup.append(val)
        rmsd_chains.append(rmsd_nup)
    rmsd_chains_all_frames.append(rmsd_chains)
print("RMSD calculation completed.")
rmsd_chains = np.array(rmsd_chains_all_frames) # shape: (n_frames, n_nups, n_chains)

np.save(f'{sim_dic}/rmsd_linkers.npy', rmsd_chains)
