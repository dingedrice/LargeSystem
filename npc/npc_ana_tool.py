import pandas as pd
import numpy as np
from Contacts.Contacts import *

df_chain_info = pd.read_pickle("/home/ed31/Documents/LargeSystem/npc/template/chain_info.pkl")

N_subunit_CA = df_chain_info.at[len(df_chain_info)-1, 'CA_end'] + 1
Nsubunits = 8
N_chain_per_subunit = len(df_chain_info)

ring_info = {
    'CR_all': ['CR', 'CR (CNC/Y)', 'CR (FG)', 'CR (unique)', 'CR (cytoplasmic filament)'],
    'IR_all': ['IR', 'IR (CNT)', 'IR (FG)'],
    'NR_all': ['NR', 'NR (CNC/Y)', 'NR (FG)', 'NR (unique)'],
    'LR_all': ['LR', 'transmembrane/IR'],
    'Bridge': ['NR-IR bridge', 'CR-IR bridge']
}

dict_chain = {ring: np.where(df_chain_info["Ring"] == ring)[0] for ring in set(df_chain_info["Ring"])}


def get_ring_indices(df_chain_info, ring_info = ring_info):
    ring_indices_all = []
    for subrings in ring_info.values():
        ring_indices = []
        start = df_chain_info[df_chain_info['Ring'].isin(subrings)]['CA_start']
        end = df_chain_info[df_chain_info['Ring'].isin(subrings)]['CA_end']
        for i, j in zip(start, end):
            ring_indices.append(np.arange(i, j+1))
        ring_indices_all.append(np.concatenate(ring_indices))
    return ring_indices_all


def get_ring_allsubunits_indices(ring_indices, ring_info = ring_info):
    # get indices of all subunits
    ring_all_indices = [[]] * len(ring_info)
    for i in range(Nsubunits):
        for j in range(len(ring_info)):
            ring_all_indices[j] = np.append(ring_all_indices[j], ring_indices[j] + i*N_subunit_CA)

    for j in range(len(ring_info)):
        ring_all_indices[j] = set(ring_all_indices[j].astype(int))

    return ring_all_indices

# Contact analysis
ring_info_reverse = {}
for k in ('CR_all', 'IR_all', 'NR_all', 'LR_all', 'Bridge'):
    for v in ring_info[k]:
        ring_info_reverse[v] = k
        
intervals = pd.IntervalIndex.from_arrays(
    df_chain_info['CA_start'],
    df_chain_info['CA_end'],
    closed='both'
)

interval_lookup = pd.Series(df_chain_info.index, index=intervals)

def idx_res2chain(i):
    return interval_lookup.loc[i%N_subunit_CA].values

class QFormation():
    @staticmethod
    def Q_timeing(data: np.ndarray):
        """The fast, vectorized method using cumsum."""
        
        t_total = data.shape[0]
        
        # Store original shape info in case data is 1D
        original_ndim = data.ndim
        if original_ndim == 1:
            data = data.reshape(-1, 1)

        # 1. Calculate the cumulative sum
        # S[t] contains the sum of data[0]...data[t]
        S = data.cumsum(axis=0)

        # 2. Create arrays for the divisors
        # t = [1, 2, ..., t_total-1]
        t = np.arange(1, t_total)
        
        # Denominators for prefix: [1, 2, ..., t_total-1]
        denom_prefix = t
        
        # Denominators for suffix: [t_total-1, t_total-2, ..., 1]
        denom_suffix = np.arange(t_total - 1, 0, -1)

        # 3. Calculate all prefix means
        # mean(data[:t]) = S[t-1] / t
        # S[:-1] gives [S[0], S[1], ..., S[t_total-2]]
        # We use [:, None] to broadcast (T,) divisors over (T, N_features)
        mean_prefix = S[:-1] / denom_prefix[:, None]

        # 4. Calculate all suffix means
        # mean(data[t:]) = (TotalSum - S[t-1]) / (t_total - t)
        total_sum = S[-1] # This is S[t_total-1]
        mean_suffix = (total_sum - S[:-1]) / denom_suffix[:, None]

        # 5. Calculate the final difference
        q_times = mean_suffix - mean_prefix
        
        # Return 1D array if original was 1D
        return q_times.ravel() if original_ndim == 1 else q_times

    @staticmethod
    def get_Q_df(contacts):
        dict_Q = {}
        dict_Q['i'] = contacts.getAtom1Array()
        dict_Q['j'] = contacts.getAtom2Array()
        dict_Q['subunit_i'] = dict_Q['i'] // N_subunit_CA
        dict_Q['subunit_j'] = dict_Q['j'] // N_subunit_CA

        # df index for residue i and j
        df_i_id = idx_res2chain(dict_Q['i'])
        df_j_id = idx_res2chain(dict_Q['j'])

        dict_Q['nup_i'] = df_chain_info.loc[df_i_id, 'Nup'].tolist()
        dict_Q['nup_j'] = df_chain_info.loc[df_j_id, 'Nup'].tolist()
        dict_Q['chainid_i'] = df_chain_info.loc[df_i_id, 'Chain ID'].tolist()
        dict_Q['chainid_j'] = df_chain_info.loc[df_j_id, 'Chain ID'].tolist()
        dict_Q['region_i'] = df_chain_info.loc[df_i_id, 'Ring'].tolist()
        dict_Q['region_j'] = df_chain_info.loc[df_j_id, 'Ring'].tolist()
        dict_Q['ring_i'] = [ring_info_reverse[i] for i in dict_Q['region_i']]
        dict_Q['ring_j'] = [ring_info_reverse[i] for i in dict_Q['region_j']]

        df_Q = pd.DataFrame(dict_Q)
        df_Q['nups'] = df_Q['nup_i'] + "-" + df_Q['nup_j']
        df_Q['chainids'] = df_Q['chainid_i'] + "-" + df_Q['chainid_j']
        df_Q['regions'] = df_Q['region_i'] + "-" + df_Q['region_j']
        df_Q['rings'] = df_Q['ring_i'] + "-" + df_Q['ring_j']

        return df_Q

    # @staticmethod
    # def categorize(df):
    #     df_intra_chain = df.query('subunit_i == subunit_j & chainid_i == chainid_j')
    #     df_inter_chain = df.query('subunit_i == subunit_j & chainid_i != chainid_j')
    #     df_inter_subunit = df.query('subunit_i != subunit_j')
    #     return df_intra_chain, df_inter_chain, df_inter_subunit

    # Qdata: shape (T, n_contacts)
    def __init__(self, Qdata:np.ndarray, contacts:Contacts):
        # self.Qdata = Qdata
        self.contacts = contacts
        # Add a row of zeros at the beginning of Qdata to remove noise
        Qdata_padd = np.vstack((np.zeros((1, Qdata.shape[1]), dtype=bool), Qdata))
        Q_tinfo = self.Q_timeing(Qdata_padd)
        self.Q_ftime = np.argmax(Q_tinfo, axis = 0)
        self.Q_max = np.max(Q_tinfo, axis = 0)
        
        self.df_Q = self.get_Q_df(self.contacts)
        self.df_Q['ftime'] = self.Q_ftime
        self.df_Q['Q_max'] = self.Q_max


        # self.t_start = t_start
        # self.Q_thresh = Q_thresh
        # idx_important = (
        #     (np.argmax(Q_tinfo, axis = 0) > self.t_start)
        #     & (np.argmax(Q_tinfo, axis = 0) < Q_tinfo.shape[0]-self.t_start)
        #     & (np.max(Q_tinfo, axis = 0) > self.Q_thresh)
        # )
        # self.idx_important = idx_important

        # self.Q_imp = Qdata[:, self.idx_important]
        # self.Q_tinfo_imp = Q_tinfo[:, self.idx_important]
        # self.contacts_imp = self.contacts.getSubContacts(self.idx_important)

        # self.df_Q_imp = self.df_Q[self.idx_important]
        # dfs = self.categorize(self.df_Q_imp)
        # self.df_Q_imp_intra_chain = dfs[0]
        # self.df_Q_imp_inter_chain = dfs[1]
        # self.df_Q_imp_inter_subunit = dfs[2]