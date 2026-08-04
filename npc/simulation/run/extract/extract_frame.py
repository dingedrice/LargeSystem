import mdtraj as md

def extract(file, ref, fileout, frame = -1):
    trj = md.load(file, top=ref)
    trj_out = trj[frame]
    trj_out.save(fileout)

# file_c1 = "../c_1/npc_trajectory.dcd"
# fileout_c1 = "c1_input.gro"
# file_c2 = "../c_2/npc_trajectory.dcd"
# fileout_c2 = "c2_input.gro"
# ref_c= "/home/ed31//Documents/LargeSystem/npc/SBM/constricted/constricted_CA.gro"

# extract(file_c1, ref_c, fileout_c1)
# extract(file_c2, ref_c, fileout_c2)

file_d1 = "../d_1/npc_trajectory.dcd"
# fileout_d1 = "d1_input.gro"
file_d2 = "../d_2/npc_trajectory.dcd"
# fileout_d2 = "d2_input.gro"
ref_d = "/home/ed31//Documents/LargeSystem/npc/SBM/dilated/dilated_CA.gro"

# extract(file_d1, ref_d, fileout_d1)
# extract(file_d2, ref_d, fileout_d2)

# file_c1 = "../c_1/npc_trajectory.dcd"
# fileout_c1 = "c1_input.gro"
# file_c2 = "../c_2/npc_trajectory.dcd"
# fileout_c2 = "c2_input.gro"
# ref_c = "/home/ed31//Documents/LargeSystem/npc/SBM/constricted/constricted_CA.gro"

extract(file_d1, ref_d, "d1_input.gro")
extract(file_d2, ref_d, "d2_input.gro")

# d1 and d2 do not follow this patter for legacy reasons.
for i in range(1, 5):
   extract(file_d1, ref_d, f"d{2*i+1}_input.gro", frame = -i*50)
   extract(file_d2, ref_d, f"d{2*i+2}_input.gro", frame = -i*50)
