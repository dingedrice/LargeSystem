# Erdong 09/30/2024, from ChatGPT 

class PDBAtom:
    """
    Class to represent an atom in a PDB file.
    Stores atomic properties like serial number, atom name, residue name, coordinates, etc.
    """
    def __init__(self, atom_line):
        """
        Initialize the PDBAtom object from a line of PDB file (ATOM/HETATM records).
        """
        self.record_type = atom_line[0:6].strip()  # ATOM or HETATM
        self.serial = int(atom_line[6:11].strip())  # Atom serial number
        self.atom_name = atom_line[12:16].strip()  # Atom name
        self.alt_loc = atom_line[16].strip()  # Alternate location indicator
        self.res_name = atom_line[17:20].strip()  # Residue name
        self.chain_id = atom_line[21].strip()  # Chain identifier
        self.res_seq = int(atom_line[22:26].strip())  # Residue sequence number
        self.i_code = atom_line[26].strip()  # Insertion code
        self.x = float(atom_line[30:38].strip())  # X coordinate
        self.y = float(atom_line[38:46].strip())  # Y coordinate
        self.z = float(atom_line[46:54].strip())  # Z coordinate
        self.occupancy = float(atom_line[54:60].strip())  # Occupancy
        self.temp_factor = float(atom_line[60:66].strip())  # Temperature factor
        self.element = atom_line[76:78].strip()  # Element symbol
        self.charge = atom_line[78:80].strip()  # Charge on the atom

    def __str__(self):
        """
        Convert the atom object back into a PDB file format.
        """
        # The adjust_PDB script writes atom names differently than the canonical way, we follow the rules of adjust_PDB.
        # The adjust_PDB script does not read charges, so the charge will not be written. 
        '''
        return f"{self.record_type:<6}{self.serial:>5}  {self.atom_name:<3}{self.alt_loc:1}" \
                f"{self.res_name:>3} {self.chain_id:1}{self.res_seq:>4}{self.i_code:1}   " \
                f"{self.x:>8.3f}{self.y:>8.3f}{self.z:>8.3f}{self.occupancy:>6.2f}" \
                f"{self.temp_factor:>6.2f}          {self.element:>2}{self.charge:>2}"
        '''
        return f"{self.record_type:<6}{self.serial:>5} {self.atom_name:<4}{self.alt_loc:1}" \
                f"{self.res_name:>3} {self.chain_id:1}{self.res_seq:>4}{self.i_code:1}   " \
                f"{self.x:>8.3f}{self.y:>8.3f}{self.z:>8.3f}{self.occupancy:>6.2f}" \
                f"{self.temp_factor:>6.2f}          {self.element:>2}"