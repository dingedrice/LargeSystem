# %%
from pdbfixer import *
import openmm.app as app

# %%
def fix(pdbfile, outputfile):
    fixer = PDBFixer(pdbfile)
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    app.PDBFile.writeFile(fixer.topology, fixer.positions, open(outputfile, 'w'))

# %%
for i in range(1, 8):
    fix(f"d{i}_input.pdb", f"d{i}_fixed.pdb")


