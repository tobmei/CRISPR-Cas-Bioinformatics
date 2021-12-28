#!/usr/bin/env python3
import re
import argparse
import logging
import sys
from Bio import SeqIO
from helpers.workflow_helpers import *
import gfapy
from helpers.input_handler import *

## INITIALIZATION
## set up argument parser and define arguments
# 3 arguments, 2 required - input_file, -output_gfa_file
parser = argparse.ArgumentParser(description="This script creates a de Bruijn graph from a reads")
parser.add_argument("--i", help="read file", required=True)
parser.add_argument("--o", help="output file", required=True)
parser.add_argument("-k", help="Substring length", default=30, required=False)

#get arguments from terminal
args = parser.parse_args()
input_file = input_in_file(args.i)
output_file = args.o
k = input_k(args.k)

## set up logging
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler('log.txt', mode='w')
handler.setFormatter(formatter)
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(screen_handler)
file = open(input_file)

#gfa initialization
gfa = gfapy.Gfa()
gfa.append("H\tVN:Z:1.0")


if __name__ == "__main__":
    #input_format variable looks for the format of file and based on it
    #is used during reading the file
    input_format = re.findall("(\.[^.]*)$", input_file)[0]
    logging.info("Creating de Bruijn graph for {} with k={}".format(input_file, k))
    
    # dictionary to store the de Bruijn graph
    dBg = {}
    all_kmers = []
    # open read file line by line (don't load the whole file into memory)
    # process the reads one after the other

    with file as handle:
        for record in SeqIO.parse(handle, input_format[1:]):
            read = record.seq # single read assigned to variable read
            kmers = generate_kmers(read, k) # split the read into kmers
            if input_format!=".fasta":
                collect_kmers(kmers,all_kmers) # add new k_mers in all_kmers variable from kmers
            else:
                all_kmers=kmers
            logging.debug("some info that might be usefull for debugging: like nr of kmers: {}".format(len(kmers)))



    # generate nodes for each kmer and store in dBg
    graphObject = create_gfa_output(all_kmers, gfa)
    gfa.to_file("output/" + output_file + ".gfa")

    logging.info(
        "\n\n\t----------------------BASIC INFORMATION---------------\n\tInput File: {}"
        "\n\tNr of reads: {}"
        "\n\tK: {}".format(input_file,len(all_kmers),k) +
        "\n\n\t----------------------INFORMATION ON GRAPH---------------\n\tOutput File: output/{}.gfa"
        "\n\tNr of Nodes: {}"
        "\n\tNr of Edges: {}".format(output_file,graphObject.nnodes(),graphObject.nedges()))

# TODO: handle different read inputs (fasta, fastq, paired, interleaved, ...)
# TODO: check if input is in supported format. Raise exception otherwise
# TODO: think about parallel processing
