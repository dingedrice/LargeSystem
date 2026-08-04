import sys
import numpy as np
from openmm.app import *
from openmm import *
from openmm.unit import *

from OpenSMOG import SBM
from OpenSMOG.OpenSMOG_Reporter import SMOGMinimizationReporter


sbm_dire = "/home/ed31/npc_SBM/"
gro_dire = "/scratch/ed31/npc_run/simulation/"
sim_index = int(sys.argv[1])
#GPU = sys.argv[2]

# CA runs
ts = 0.0005
rc = 1.1

sbm_grofile = f"{gro_dire}/d{(sim_index+1)//2}_input.gro"
    
sbm_topfile = f"{sbm_dire}/constricted/constricted_CA.top" # Change this for different force field
sbm_xmlfile = f"{sbm_dire}/constricted/constricted_CA.xml" # Change this for different force field


sbm = SBM(name='npc', time_step=ts, collision_rate=1.0, r_cutoff=rc, temperature=0.6, cmm=False, pbc=False)
sbm.setup_openmm(platform='cuda')
sbm.saveFolder(f"{sim_index}")

sbm.loadSystem(Grofile=sbm_grofile, Topfile=sbm_topfile, Xmlfile=sbm_xmlfile)

sbm.createSimulation()
try:
    sbm.loadCheckpoint(f"{sim_index}/smog.chk")
except:
    sbm.minimize(tolerance=1)

sbm.createReporters(trajectory=True, energies=True, energy_components=True, interval=10**4, checkpointInterval=10**4)

sbm.run(4*10**7, interval = 10**4) # Run on ctbp GPUs
# sbm.run(8*10**7, interval = 10**4) # Run on commons GPUs, roughly twice the steps
