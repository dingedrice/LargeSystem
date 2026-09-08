'''
This file is to calculate the ring COM and the diameter of different rings from the COM data of the NPC system.
Example usage can be found in the notebook Fig.ipynb
'''
from npc_ana_tool import *

chain_range = np.append(df_chain_info['CA_start'].values, [N_subunit_CA])   
mass = np.diff(chain_range)

M_subunit = mass.sum()


def get_ring_com(com_file, mass, dict_chain, ring_info):
    com = np.load(com_file)
    ring_com = {}
    for key in ring_info.keys():
        if key == 'Rings':
            continue
        ring = ring_info[key]

        chain_indices = []
        for chain in ring:
            chain_indices += list(dict_chain[chain])
        chain_indices = np.array(chain_indices)
        # for i in range(1, 8):
        #     chain_indices.append(chain_indices[0] + N_chain_per_subunit *i)
        # chain_indices = np.concatenate(chain_indices)
        # chain_indices = chain_indices.reshape(8, -1)

        # mass_ring = mass[chain_indices].reshape(1, *mass[chain_indices].shape, 1)
        mass_ring = mass[chain_indices]
        # print(mass_ring.shape)
        mass_ring_total = mass_ring.sum()
        # print(mass_ring_total.shape)
        # print(com[:, chain_indices, :].shape)
        
        ring_com[key] = (com[:, chain_indices, :] * mass_ring[:, None, None]).sum(axis = 1) / mass_ring_total
    return ring_com


# The input should be of a certain ring from ring_com
def get_diameter(diameter_data):
    diameter = []
    for id in range(4):
        diameter.append(np.linalg.norm(diameter_data[:, id] - diameter_data[:, id+4], axis = -1))
    return np.array(diameter).T

