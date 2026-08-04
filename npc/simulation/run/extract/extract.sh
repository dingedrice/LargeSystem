#!/bin/bash

# Generate the files
python extract_frame.py
# Change the size of the box
ls *input.gro | xargs -I {} sed -i '$c\200.00 200.00 200.00' {} 
