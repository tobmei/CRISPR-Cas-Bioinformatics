#!/usr/bin/env python3

import argparse
import glob
import re
import os
import subprocess
import logging
import sys
import multiprocessing

parser = argparse.ArgumentParser(
    description="")

parser.add_argument("--metagenomes", help="input jgi metagenomes (i.e. gzipped tar archives", nargs='+', required=True)
parser.add_argument("--output", help="path to output folder", required=True)
parser.add_argument("--workers", help="number of parallel processes", required=True)

args = parser.parse_args()
metagenomes = args.metagenomes
output_dir = args.output
workers = int(args.workers)

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler('log.txt', mode='w')
handler.setFormatter(formatter)
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(screen_handler)

crisprcasidentifier = "/home/tmeier/CRISPRCasIdentifier/crispr-cas-identifier/CRISPRcasIdentifier.py"


def call_subprocess(command):
    cp = multiprocessing.current_process()
    logging.info("{} | {}".format(cp.name, command))
    command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    process_output, stderr = command_line_process.communicate()
    logging.info("{} finished: {}".format(cp.name, command_line_process.returncode))
    #logging.info("{} finished: {}".format(cp.name, stderr))

    return command_line_process.returncode


def analysis(metagenome):
    ## get sample id
    sample_id = re.match(re.compile(r".*/([0-9]*)\.tar\.gz$"), metagenome).group(1)

    ## extract contigs (*.a.fna) from tar archive to output folder
    untar_contigs = ["tar", "-C", output_dir, "-xzf", metagenome, "{}/{}.a.fna".format(sample_id, sample_id)]
    returncode = call_subprocess(untar_contigs)
    contig_file = "{}{}/{}.a.fna".format(output_dir, sample_id, sample_id)

    ## run CRISPRCasIdentifier on contigs
    crisprcasid = ["python", crisprcasidentifier, "-f", contig_file, "-p", "-o",
                   "crisprcasidentifier_{}".format(sample_id),
                   "-st", "dna", "-sc", "partial", "-m", "mixed",
                   "-ho", "{}{}".format(output_dir,sample_id),
                   "-co", "{}{}".format(output_dir,sample_id),]
    call_subprocess(crisprcasid)

    ## remove extracted contig file
    rm_contigs = ["rm", contig_file]
    call_subprocess(rm_contigs)


if __name__ == "__main__":

    # create a pool of workers
    print("creating multiprocessing pool with {} workers...".format(workers))
    pool = multiprocessing.Pool(processes=workers)
    for metagenome in metagenomes:  ## 'metagenome' == jgt tar archive (3330000123.tar.gz)
        pool.apply_async(analysis, args=(metagenome,))
    pool.close()
    pool.join()
