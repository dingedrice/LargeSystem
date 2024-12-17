# %%
import sys
import mdtraj as md

if len(sys.argv) > 3:
    print("Error, only one input PDB file allowed")
    sys.exit()

filein = sys.argv[1]
fileout = sys.argv[2]

# Generate the sequence for the PDB file
def write_SEQRES(trj, fout):
    seq = list(map(lambda x: x.name, trj.topology.residues))
    chain_id = trj.topology.chain(0).chain_id
    i = 0
    with open(fout, "w") as f:
        for i in range(0, len(seq), 13):
            residue_group = seq[i:i + 13]
            f.write(f"SEQRES {i//13 + 1:>3} {chain_id} {len(seq):>4}  {' '.join(residue_group)}")
            f.write("\n")

t = md.load(filein)
write_SEQRES(t, fileout)


