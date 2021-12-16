#!/usr/bin/env python3

import multiprocessing
import subprocess
import sys
import glob
import re
import os

processes_nr = 20

def tool(contig):
    print("processing: {}".format(contig))
    ncbi = re.match("^(.*)_.*",os.path.basename(contig)).group(1)
    output = "/data/tobias/ncbi_assemblies/opt_assemblies_viral_contigs"
    #output = "/data/tobias/ncbi_crispr_arrays/protospacers
    subprocess.call("Rscript /home/tmeier/misc/run_virfinder.R {} {} {}".format(contig,output,ncbi), shell=True)
    subprocess.call("awk -F ',' '!/name/{{print $2}}' {}/{}_virfinder_out | sed 's/\"//g' > {}/{}_ids.txt".format(output,ncbi,output,ncbi), shell=True)
    subprocess.call("awk -F '>' 'NR==FNR{{ids[$0]; next}} NF>1{{f=($2 in ids)}} f'  %s/%s_ids.txt contigs_1000 / %s_contigs1000.fasta > %s/%s_contigs_viral.fasta" % (output,ncbi,ncbi,output,ncbi),shell=True)

def multi():
    # create a pool of workers
    print("creating multiprocessing pool with {} workers...".format(processes_nr))
    pool = multiprocessing.Pool(processes=processes_nr)
    for contig in glob.glob(sys.argv[1]):
        pool.apply_async(tool, args=(contig,))
    pool.close()
    pool.join()


multi()

