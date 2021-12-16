from Bio import SeqIO
import sys
import os
import re
import subprocess
import multiprocessing


protospacer_contigs_file = sys.argv[1] #path to rsr.fastas
blastdb = sys.argv[2]
assemblies = sys.argv[3]
output_dir = sys.argv[4]

