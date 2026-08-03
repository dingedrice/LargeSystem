'''
This file is to calculate RMSD, Q, and COM of the NPC system.
It uses the Maanalysis package instead of mdtraj for better memory efficiency.
The code is modified by Gemini from my old code using mdtraj.
'''

import sys
sys.path.append('/home/ed31/Documents/LargeSystem/npc/')
from npc_ana_tool import *

import MDAnalysis as mda
from MDAnalysis.analysis import rms, align
from MDAnalysis.lib.distances import calc_bonds

class Indices:
    def get_region_indices(self, region):
        df_tmp = self.df_chain_info[region]
        id_single_subunit = []
        for i, j in zip(df_tmp['CA_start'], df_tmp['CA_end']):
            id_single_subunit += list(range(i, j+1))
        id_single_subunit = np.array(id_single_subunit).flatten()
        id_all_subunits = np.array([id_single_subunit + k*N_subunit_CA for k in range(Nsubunits)])
        return id_all_subunits

    def get_chain_indices(self):
        self.id_chain = []
        for start, end in zip(self.df_chain_info['CA_start'], self.df_chain_info['CA_end']):
            tmp_list = [np.arange(start, end+1) + k*N_subunit_CA for k in range(Nsubunits)]
            self.id_chain.append(np.array(tmp_list))

    def __init__(self, df_chain_info = df_chain_info, ring_info = ring_info):
        self.df_chain_info = df_chain_info
        self.ring_info = ring_info

        self.id = {}
        self.id['subunit'] = np.arange(Nsubunits*N_subunit_CA).reshape(Nsubunits, -1)
        self.id['CR'] = self.get_region_indices(df_chain_info['Ring'].isin(ring_info['CR_all']))
        self.id['IR'] = self.get_region_indices(df_chain_info['Ring'].isin(ring_info['IR_all']))
        self.id['NR'] = self.get_region_indices(df_chain_info['Ring'].isin(ring_info['NR_all']))
        self.id['LR'] = self.get_region_indices(df_chain_info['Ring'].isin(ring_info['LR_all']))

        self.get_chain_indices()


# RMSD

def get_rmsd_regions_frame(trj: mda.Universe, ref: mda.Universe, indices: Indices):
    rmsd_regions = {}
    for region_name, region_ids in indices.id.items():
        rmsd_subunits = []
        for subunit_id in region_ids:
            ag_u = trj.atoms[subunit_id]
            ag_ref = ref.atoms[subunit_id]
            # rms.rmsd calculates single-frame alignment and RMSD
            val = rms.rmsd(ag_u.positions, ag_ref.positions, superposition=True)
            rmsd_subunits.append(val)
        rmsd_regions[region_name] = np.array(rmsd_subunits)
    return rmsd_regions # Dict of region_name 

def get_rmsd_chains_frame(trj: mda.Universe, ref: mda.Universe, indices: Indices):
    """Calculates RMSD for all chains for a single trajectory frame."""
    rmsd_chains = []
    for id_nup in indices.id_chain:
        rmsd_nup = []
        for chain in id_nup:
            ag_u = trj.atoms[chain]
            ag_ref = ref.atoms[chain]
            val = rms.rmsd(ag_u.positions, ag_ref.positions, superposition=True)
            rmsd_nup.append(val)
        rmsd_chains.append(rmsd_nup)
    return np.array(rmsd_chains) # Array of shape (101, 8)

class RMSDAnalysis:
    def __init__(self, rmsd_regions: dict, rmsd_chains: np.array):        
        self.rmsd_regions = rmsd_regions
        self.rmsd_chains = rmsd_chains


# Q

def get_qi_frame(trj: mda.Universe, d_native, idx1, idx2):
    pos = trj.atoms.positions
    # Fast distance calculation between pairs of coordinates
    d = calc_bonds(pos[idx1], pos[idx2])
    return d / d_native  


# COM

def get_chain_COM_fit_frame(trj: mda.Universe, ref: mda.Universe, indices: Indices):
    # 1. Superpose current frame to reference
    align.alignto(trj.atoms, ref.atoms, select="all")
        
    # 2. Calculate COM for each chain in this frame
    # .center_of_geometry() matches your original .mean(axis=1) logic
    frame_com_chains = []
    for id_nup in indices.id_chain:
        frame_com_nup = []
        for chain in id_nup:
            # We select the atoms for this chain and get their mean position
            com = trj.atoms[chain].center_of_geometry()
            frame_com_nup.append(com)
        frame_com_chains.append(frame_com_nup)
    return np.array(frame_com_chains) # Shape: (101, 8, 3)


# Wrap

def get_rmsd(trj: mda.Universe, ref: mda.Universe, indices: Indices):
    rmsd_regions_all = {region: [] for region in indices.id.keys()}
    rmsd_chains_all = []
    for ts in trj.trajectory:
        # indicate progress
        if ts.frame % 100 == 0:
            print(f"Processing frame {ts.frame}/{len(trj.trajectory)}")
        reg_rmsd = get_rmsd_regions_frame(trj, ref, indices)
        for region, values in reg_rmsd.items():
            rmsd_regions_all[region].append(values)
        ch_rmsd = get_rmsd_chains_frame(trj, ref, indices)
        rmsd_chains_all.append(ch_rmsd)
    print("RMSD calculation completed.")
    for region in rmsd_regions_all:
        rmsd_regions_all[region] = np.array(rmsd_regions_all[region]) # (n_frames, n_subunits)
    rmsd_chains_all = np.array(rmsd_chains_all) # (n_frames, 101, 8)
    return RMSDAnalysis(rmsd_regions_all, rmsd_chains_all)

def get_qi(trj: mda.Universe, d_native, idx1, idx2):
    qi_all = []
    for ts in trj.trajectory:
        # indicate progress
        if ts.frame % 100 == 0:
            print(f"Processing frame {ts.frame}/{len(trj.trajectory)}")
        qi = get_qi_frame(trj, d_native, idx1, idx2)
        qi_all.append(qi)
    print("Q fraction calculation completed.")
    return np.array(qi_all) # (n_frames, n_contacts)

def get_chain_COM_fit(trj: mda.Universe, ref: mda.Universe, indices: Indices):
    com_chains_all = []
    for ts in trj.trajectory:
        # indicate progress
        if ts.frame % 100 == 0:
            print(f"Processing frame {ts.frame}/{len(trj.trajectory)}")
        com = get_chain_COM_fit_frame(trj, ref, indices)
        com_chains_all.append(com)
    print("COM calculation completed.")
    return np.array(com_chains_all) # (n_frames, 101, 8, 3)


if __name__ == "__main__":
    import pickle
    import os

    sim_dic = sys.argv[1]
    sim_init = sys.argv[2]

    npc_indices = Indices()
    work_dir = '/home/ed31/Documents/LargeSystem/npc'
    reffile = f"{work_dir}/constricted_CA.pdb"
    ref_c0 = mda.Universe(reffile)

    Qthreshold = 1.2

    # Combine all trajectory segments into a single list
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

    dire_Q = "/home/ed31/Documents/LargeSystem/npc/SBM/dual_basin/"
    with open(f"{dire_Q}/contact_DB_uniq_c.pkl", "rb") as f:
        cont_uniq_c = pickle.load(f)

    contact_indices = cont_uniq_c.getIndices()
    d_native = cont_uniq_c.getDistanceArray() * 10  # Convert to Angstroms

    # Split indices into pair groups for fast array indexing
    idx1 = contact_indices[:, 0]
    idx2 = contact_indices[:, 1]

    # --- Initialize Accumulators ---
    rmsd_regions_all = {region: [] for region in npc_indices.id.keys()}
    rmsd_chains_all = []
    qi_all = []
    com_chains_all = []

    # --- Unified External Trajectory Loop ---
    for ts in trj.trajectory:
        # indicate progress
        if ts.frame % 100 == 0:
            print(f"Processing frame {ts.frame}/{len(trj.trajectory)}")
        # 1. RMSD Regions
        reg_rmsd = get_rmsd_regions_frame(trj, ref_c0, npc_indices)
        for region, values in reg_rmsd.items():
            rmsd_regions_all[region].append(values)
            
        # 2. RMSD Chains
        ch_rmsd = get_rmsd_chains_frame(trj, ref_c0, npc_indices)
        rmsd_chains_all.append(ch_rmsd)
        
        # 3. Q fraction (Uncomment if contacts object is actively used)
        qi = get_qi_frame(trj, d_native, idx1, idx2)
        qi_all.append(qi)
        
        # 4. COM (Note: align.alignto inside here modifies trj coordinates in-place 
        # for this frame step, which is overwritten safely on the next loop iteration)
        com = get_chain_COM_fit_frame(trj, ref_c0, npc_indices)
        com_chains_all.append(com)
    print("Trajectory analysis completed.")
    # --- Format final arrays ---

    for region in rmsd_regions_all:
        rmsd_regions_all[region] = np.array(rmsd_regions_all[region]) # (n_frames, n_subunits)
    rmsd_chains_all = np.array(rmsd_chains_all) # (n_frames, 101, 8)
    rmsd_all = RMSDAnalysis(rmsd_regions_all, rmsd_chains_all)

    qi_all = np.array(qi_all)                 # (n_frames, n_contacts) Distance ratio
    Qi_all = qi_all < Qthreshold  # Boolean array for Q fraction

    Q_form = QFormation(Qi_all, cont_uniq_c)

    com_chains_all = np.array(com_chains_all)   # (n_frames, 101, 8, 3)
    
    # --- Save results ---
    with open(f"{sim_dic}/rmsd.pkl", "wb") as f:
        pickle.dump(rmsd_all, f)

    np.save(f"{sim_dic}/qi_DB_c.npy", qi_all)
    np.save(f"{sim_dic}/Qi_DB_c.npy", Qi_all)
    with open(f"{sim_dic}/Q_form.pkl", "wb") as f:
        pickle.dump(Q_form, f)

    np.save(f"{sim_dic}/chain_COM_fit2c.npy", com_chains_all)