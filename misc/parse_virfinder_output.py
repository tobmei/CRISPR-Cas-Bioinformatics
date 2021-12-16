import argparse
import re


parser = argparse.ArgumentParser(description="This script does the following...")

parser.add_argument("--input", nargs='+', required=True)
parser.add_argument("--assembler", required=True)
args = parser.parse_args()

print("parameter_set,contig_id,length,coverage,score,pvalue")
for file in args.input:
    with open(file) as handle:
        parameter_set = re.match(".*\/([0-9]+)_virfinder_out",file).group(1)
        handle.readline() # skip header line
        for line in handle:
            line = line.strip("\n").replace('"','').split(",")
            fasta_header = line[1].split()
            if args.assembler == 'mega':
                contig_id = fasta_header[0]
                coverage = str(round(float(re.match("multi=(.*)", fasta_header[2]).group(1)),2))
            elif args.assembler == 'meta':
                contig_id = fasta_header[0].split("_")[1]
                coverage = str(round(float(fasta_header[0].split("_")[5]),2))
            length = line[2]
            score = line[3]
            pvalue = line[4]
            qvalue = float(line[5])

            if qvalue <= 0.05:  # fdr of 5%
                print(parameter_set+","+contig_id+","+length+","+coverage+","+score+","+pvalue)


