import sys
import numpy as np
from openmm.app import *
from openmm import *
from openmm.unit import *

from OpenSMOG import SBM
from OpenSMOG.OpenSMOG_Reporter import SMOGMinimizationReporter


dire = "/home1/erdong/SBM_npc"
name = sys.argv[1]
GPU = sys.argv[2]
sim_index = sys.argv[3]

# CA runs
ts = 0.0005
rc = 1.1

if name == 'd2c':
    sbm_grofile = f"{dire}/dilated_CA.gro"
    sbm_topfile = f"{dire}/constricted_CA.top"
    sbm_xmlfile = f"{dire}/constricted_CA.xml"
elif name == 'c2d':
    sbm_grofile = f"{dire}/constricted_CA.gro"
    sbm_topfile = f"{dire}/dilated_CA.top"
    sbm_xmlfile = f"{dire}/dilated_CA.xml"
elif name == 'c':
    sbm_grofile = f"{dire}/constricted_CA.gro"
    sbm_topfile = f"{dire}/constricted_CA.top"
    sbm_xmlfile = f"{dire}/constricted_CA.xml"
elif name == 'd':
    sbm_grofile = f"{dire}/dilated_CA.gro"
    sbm_topfile = f"{dire}/dilated_CA.top"
    sbm_xmlfile = f"{dire}/dilated_CA.xml"


sbm = SBM(name='npc', time_step=ts, collision_rate=1.0, r_cutoff=rc, temperature=0.6, cmm=False, pbc=False)
sbm.setup_openmm(platform='hip', GPUindex=GPU)
sbm.saveFolder(f"{name}_{sim_index}")

sbm.loadSystem(Grofile=sbm_grofile, Topfile=sbm_topfile, Xmlfile=sbm_xmlfile)

sbm.createSimulation()
sbm.loadCheckpoint(f"{name}_{sim_index}/smog.chk")
#sbm.minimize(tolerance=1)

sbm.createReporters(trajectory=True, energies=True, energy_components=True, interval=10**5, checkpointInterval=10**6)
sbm.run(5*10**7, interval = 10**5)
