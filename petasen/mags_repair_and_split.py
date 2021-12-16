#!/usr/bin/env python3

import argparse
import re
import sys

parser = argparse.ArgumentParser(description="This script does the following...")

parser.add_argument("--output", help="path to output", required=True)


args = parser.parse_args()
out = args.output

#header lines look like this
#mags_1/000075500[...]nmags_1/ERR1953522_bin.29.fa0000755001573200023110000520220213405547735015002 0ustar  aalmeidametagen>NODE_3080_length_20357_cov_3.322825

#delete everything preceeding the >
#split into separate bins

first_header = True
first_file = None

for line in sys.stdin:
    line = str(line).strip()

    if re.match(".*mags.*", line): #header line that needs to be corrected
        fasta_header = re.match(".*(>.*)", line).group(1)
        acc = re.match(".*\/(.*_bin\..*)\.fa.*", line).group(1)

        f = open("{}/{}.fa".format(out,acc),"w")
        f.write(fasta_header+"\n")


    else:
        f.write(line+"\n")

f.close()
