# Calculate the RMSD and COM of the NPC system with regard to the two end states.
import sys
sys.path.append("/home/ed31/Documents/LargeSystem/npc")
from trj_ana_tool import *
import pickle

npc_indices = Indices()

work_dir = '/home/ed31/Documents/LargeSystem/npc'
reffile = f"{work_dir}/constricted_CA.pdb"
ref_c0 = mda.Universe(reffile)

testfile = f"{work_dir}/dilated_CA.pdb"
test_d0 = mda.Universe(testfile)

# RMSD
cd_crystal_rmsd = get_rmsd(test_d0, ref_c0, npc_indices)

# COM
d_crystal_COM = get_chain_COM_fit(test_d0, ref_c0, npc_indices)
c_crystal_COM = get_chain_COM_fit(ref_c0, ref_c0, npc_indices)
cd_crystal_COM = np.vstack([d_crystal_COM, c_crystal_COM])

with open(f"cdcrystal_rmsd.pkl", "wb") as f:
    pickle.dump(cd_crystal_rmsd, f)

np.save(f"cdcrystal_COM.npy", cd_crystal_COM)
