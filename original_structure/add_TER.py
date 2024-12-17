import sys

if len(sys.argv) > 3:
    print("Error, only one input PDB file allowed")
    sys.exit()

filein = sys.argv[1]
fileout = sys.argv[2]

res_seq = 4
chain = 'A'

with open(fileout, 'w') as fout:
    with open(filein, 'r') as fin:
        for line in fin:
            if line.startswith("ATOM"):
                res_seq_new = int(line[22:26].strip())
                if res_seq_new - res_seq > 1 or res_seq_new < res_seq or line[21].strip() != chain:
                    fout.write("TER\n")
                    chain = line[21].strip()
                res_seq = res_seq_new
            fout.write(line)            


