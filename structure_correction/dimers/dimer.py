import numpy as np
import sys
sys.path.append("/mnt/e/LargeSystem/npc/")

from init import *

write_subunits("../refine_structures/constricted/constricted_final.pdb", "constricted_dimer.pdb", C_CONSTRICTED_A, 2)
write_subunits("../refine_structures/dilated/dilated_final.pdb", "dilated_dimer.pdb", C_DILATED_A, 2)
