import sys
import numpy as np


def minimize(sbm,tolerance=1.0,maxIterations=0,reportInterval=100,minTrajectory=None):
    print("Starting minimization using L-BFGS method")
    print("step, energy")
    R"""Wrapper for L-BFGS energy minimization.

        Args:

        tolerance (float, required):
            Stopping criteria value between iterations. When the error between iteration is below this value, the minimization stops. (Default value: :code:`1.0`).
        maxIteration (int, optional):
            Number of maximum steps to be performed in the minimization simulation. (Default value: :code:`0`).   
        reportInterval (int, optional):
            Frequency to write energy to screen. (Default value: :code:`100` steps).   
        minTrajectory (str, optional):
            Name of file to write trajectory. If set to :code:`None`, then no file would be written. (Default value: :code:`None`).   
    """
    reporter = SMOGMinimizationReporter()
    reporter.reportInterval=reportInterval

    reporter.mintraj = None

    if minTrajectory != None:
        trajfile = open(minTrajectory, "wb")
        reporter.mintraj=dcdfile.DCDFile(trajfile, sbm.Top.topology, 1, 0, interval=reportInterval)

    sbm.simulation.minimizeEnergy(tolerance=tolerance,maxIterations=maxIterations,reporter=reporter)
    # it is very important that we reset the velocities. minimization warps the velocity values
    # sbm.simulation.context.setVelocitiesToTemperature(sbm.temperature)
    if minTrajectory != None:
        trajfile.close()
    print("Minimization completed")

def step_minimize(sbm, tolerance=1.0,maxIterations=0,reportInterval=100,minTrajectory=None):

    exclude_volume = sbm.system.getForces()[1] # the index of the exclude_volume force is 1
    _, C12_sqrt = exclude_volume.getParticleParameters(0) # 0 can be any value, all particles give the same LJ parameters

    coefficent = np.linspace(0.25, 1.25, 5)**6

    if '.' in minTrajectory:
        trajectory = minTrajectory.split('.')
        traj_name = [f"{trajectory[0]}_{step}.{trajectory[1]}" for step in range(len(coefficent))]
    else:
        traj_name = [f"{minTrajectory}_{step}.dcd" for step in range(len(coefficent))]

    for step in range(len(coefficent)):
        
        for i in range(0, exclude_volume.getNumParticles()):
            exclude_volume.setParticleParameters(i, (0.0, coefficent[step]*C12_sqrt))
        exclude_volume.updateParametersInContext(sbm.simulation.context)
        minimize(sbm, tolerance = tolerance, maxIterations = maxIterations, reportInterval=reportInterval, minTrajectory=traj_name[step])

    # sbm.simulation.context.setVelocitiesToTemperature(sbm.temperature)    
    

from openmm.app import *
from openmm import *
from openmm.unit import *
from OpenSMOG import SBM
from OpenSMOG.OpenSMOG_Reporter import SMOGMinimizationReporter

freeze = np.loadtxt("freeze_dilated.ndx", dtype=int) - 1

sbm_AA = SBM(name='emin', time_step=0.002, collision_rate=1.0, r_cutoff=0.65, temperature=0.831, cmm=False, pbc=True)
sbm_AA.setup_openmm(platform='cpu')
sbm_AA.saveFolder("steps/")
sbm_AA_grofile = 'dilated_dimer.gro'
sbm_AA_topfile = '/work/cms16/ed31/npc/dilated/SBM_L/openmm_del/dilated.top'
sbm_AA_xmlfile = '/work/cms16/ed31/npc/dilated/SBM_L/openmm_del/dilated.xml'

sbm_AA.loadSystem(Grofile=sbm_AA_grofile, Topfile=sbm_AA_topfile, Xmlfile=sbm_AA_xmlfile)

for i in freeze:
    sbm_AA.system.setParticleMass(i, 0*amu)

sbm_AA.createSimulation()
step_minimize(sbm_AA, tolerance=1.0, reportInterval=10, minTrajectory="steps/emin")
sbm_AA.simulation.saveState("steps/emin.xml")

xyz = sbm_AA.simulation.context.getState(getPositions=True).getPositions(asNumpy=True).value_in_unit(nanometer)
import mdtraj as md
state_gro = md.load(sbm_AA_grofile)
state_gro.xyz = np.array([xyz])
state_gro.save('steps/emin.gro')

V = sbm_AA.simulation.context.getState(getEnergy = True).getPotentialEnergy().value_in_unit(kilojoule/mole)
print(f"Final potentail energy: {V}")
