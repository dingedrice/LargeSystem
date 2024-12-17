# Erdong 09/30/2024, from ChatGPT 
import numpy as np

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
        # self.serial = int(atom_line[6:11].strip())  # Atom serial number
        self.serial = atom_line[6:11].strip()  # Atom serial number
        self.atom_name = atom_line[12:16].strip()  # Atom name
        self.alt_loc = atom_line[16].strip()  # Alternate location indicator
        # self.res_name = atom_line[17:20].strip()  # Residue name
        self.res_name = atom_line[17:21].strip()  # Residue name
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
        # The adjust_PDB script writes atom names and residue names differently than the canonical way, we follow the rules of adjust_PDB.
        # The adjust_PDB script does not read charges, so the charge will not be written. 
        '''
        return f"{self.record_type:<6}{self.serial:>5}  {self.atom_name:<3}{self.alt_loc:1}" \
                f"{self.res_name:>3} {self.chain_id:1}{self.res_seq:>4}{self.i_code:1}   " \
                f"{self.x:>8.3f}{self.y:>8.3f}{self.z:>8.3f}{self.occupancy:>6.2f}" \
                f"{self.temp_factor:>6.2f}          {self.element:>2}{self.charge:>2}"
        '''
        return f"{self.record_type:<6}{self.serial:>5} {self.atom_name:<4}{self.alt_loc:1}" \
                f"{self.res_name:<4}{self.chain_id:1}{self.res_seq:>4}{self.i_code:1}   " \
                f"{self.x:>8.3f}{self.y:>8.3f}{self.z:>8.3f}{self.occupancy:>6.2f}" \
                f"{self.temp_factor:>6.2f}          {self.element:>2}"
    
    def tostring_PDB(self, charge = False):
        string = f"{self.record_type:<6}{self.serial:>5}  {self.atom_name:<3}{self.alt_loc:1}" \
                    f"{self.res_name:>3} {self.chain_id:1}{self.res_seq:>4}{self.i_code:1}   " \
                    f"{self.x:>8.3f}{self.y:>8.3f}{self.z:>8.3f}{self.occupancy:>6.2f}" \
                    f"{self.temp_factor:>6.2f}          {self.element:>2}"
        if charge:
            return f"{string}{self.charge:>2}"
        else:
            return string

# Obtained from axis.ipynb
C_DILATED_A = np.array([993.60, 993.60, 0.00])
C_CONSTRICTED_A = np.array([970.56, 970.56, 0.00])

# Rotate counterclockwise around the z-axis by theta, right multiplied
def Rotate_Z(theta = np.pi/4):
    R = np.array([np.cos(theta), np.sin(theta), 0, -np.sin(theta), np.cos(theta), 0, 0, 0, 1]).reshape(3, 3)
    return R

def read_template(file):
    template = []
    with open(file, 'r') as fin:
        for line in fin:
            dat = line.strip().split()
            if len(dat) > 0 and (dat[0] == "ATOM" or dat[0] == "HETATM"):
                template.append(PDBAtom(line))
            elif len(dat) > 0 and dat[0] == "TER":
                template.append(dat[0])
    return template

# Write a subunit with the given coordinates (in A)
def write_subunit(templfile, outfile, coord):
    template = read_template(templfile)

    with open(outfile, 'w') as fout:
        fout.write("REMARK File generated with write_subunits function in /mnt/e/LargeSystem/npc/init.py\n")
        fout.write(f"REMARK Generate one subunit using {templfile} as a template\n")

        atom_index = 0
        for atom in template:
            if atom == "TER":
                fout.write("TER\n")
            else:
                atom.x, atom.y, atom.z = coord[atom_index]
                atom_index += 1
                fout.write(str(atom) + '\n')
        fout.write("END\n")
    return template

# Rotate counterclockwise around the z-axis by 45 degrees each time
def write_subunits(templfile, outfile, center, n):
    template = read_template(templfile)

    with open(outfile, 'w') as fout:
        fout.write("REMARK File generated with write_subunits function in /mnt/e/LargeSystem/npc/init.py\n")
        fout.write(f"REMARK Generate {n} subunit(s) from rotation of {templfile}\n")
        for k in range(n):

            R = Rotate_Z(k*np.pi/4)
            for atom in template:
                if atom == "TER":
                    fout.write("TER\n")
                else:
                    atom.x, atom.y, atom.z = (np.array([atom.x, atom.y, atom.z]) - center)@R + center
                    fout.write(str(atom) + '\n')
            if k != n-1:
                fout.write("TER\n")
        fout.write("END\n")
    return template

N_ATOMS_SUBUNIT = 617133