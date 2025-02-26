import numpy as np
import mdtraj as md

def reorganize_pdb(pdb_templ, pdb_input, pdb_output):
    input = md.load(pdb_input)
    templ = md.load(pdb_templ)
    atom_list = list(map(str, input.top.atoms))

    indices_match = []
    for i in templ.top.atoms:
        try:
            indices_match.append(atom_list.index(str(i)))
        except:
            pass
    indices_match = np.array(indices_match)
    templ.xyz[0] = input.xyz[0][indices_match]
    templ.save_pdb(pdb_output)