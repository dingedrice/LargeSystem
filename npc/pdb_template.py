
import pandas as pd
import numpy as np

df_chain_info = pd.read_pickle("template/chain_info.pkl")
N_subunit = 78030
ter_list = []
for i in range(8):  
    ter_list = np.append(ter_list, N_subunit*i + np.array(df_chain_info['CA_end'] + 1))

ter_list = ter_list.astype(int)

def gro2pdb(grofile, pdbfile, ter_list):
    count = 0   # index of chain
    N_line = 0  # index of line
    res_seq = 0 # index of residue within the chain

    TER = ter_list[count]

    record_type = 'ATOM'
    alt_loc = ' '
    chain_id = chr(65+count%26) # A-Z
    i_code = ' '
    occupancy = ''
    temp_factor = ''
    element = 'C'
    with open(pdbfile, 'w') as fout:
        with open(grofile, 'r') as fin:
            for line in fin:
                N_line += 1
                
                if N_line < 3 or N_line == N_subunit * 8 + 3:
                    continue

                serial = int(line[15:20])
                atom_name = line[10:15].strip()
                res_name = line[5:10].strip()
                res_seq += 1
                
                x = float(line[20:28]) * 10
                y = float(line[28:36]) * 10
                z = float(line[36:44]) * 10
                
                s = f"{record_type:<6}{serial:>5} {atom_name:<4}{alt_loc:1}" \
                f"{res_name:<4}{chain_id:1}{res_seq:>4}{i_code:1}   " \
                f"{x:>8.3f}{y:>8.3f}{z:>8.3f}{occupancy:>6}" \
                f"{temp_factor:>6}          {element:>2}\n"

                fout.write(s)
                i_atom = N_line - 2

                if i_atom == TER:
                    count += 1
                    if count < len(ter_list):
                        TER = ter_list[count]
                        fout.write("TER\n")
                        chain_id = chr(65+count%26)
                        res_seq = 0
                    else:
                        break
        fout.write("END\n")

gro2pdb("SBM/constricted/constricted_CA.gro", "constricted_CA.pdb", ter_list)
gro2pdb("SBM/dilated/dilated_CA.gro", "dilated_CA.pdb", ter_list)


