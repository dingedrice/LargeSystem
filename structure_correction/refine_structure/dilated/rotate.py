import sys
sys.path.append("/mnt/e/LargeSystem/npc/")

from init import *

# Rotate clockwise around the z-axis by 45 degrees, right multiplied
A = Rotate_Z(theta = -np.pi/4)

template = read_template("d7_fixed.pdb")
# R = Rotate_Z(k*np.pi/4)
with open ("d7_fixed_rotated.pdb", 'w') as fout:
    for atom in template:
        if atom == "TER":
            fout.write("TER\n")
        else:
            atom.x, atom.y, atom.z = (np.array([atom.x, atom.y, atom.z]) - C_DILATED_A)@A + C_DILATED_A
            fout.write(str(atom) + '\n')

