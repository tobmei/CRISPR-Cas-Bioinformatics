#!/usr/bin/env python3


import multiprocessing
import subprocess
import argparse
import re
import glob
import logging
import sys
import os

## extract .fna from tar archive and run prodigal
##

parser = argparse.ArgumentParser(description="This script runs hmmsearch on jgi metagenomes")

parser.add_argument("--input", help="input directory with jgi tar.gz archives", required=True)
parser.add_argument("--output", help="path to output", required=True)
parser.add_argument("--hmm", help="path to profiles", required=True)

args = parser.parse_args()

dir = args.input
out = args.output
hmms = args.hmm

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler('log.txt', mode='w')
handler.setFormatter(formatter)
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(screen_handler)

processes_nr = 150


def pipeline_pipes(archive,hmm):
    cp = multiprocessing.current_process().name
    jgi_id = re.search(re.compile(".*\/(33.*)\.tar\.gz"), archive).group(1)
    profile_name = re.search(re.compile(".*\/(.*)\.hmm$"), hmm).group(1)

    # ouput file exists?
    if os.path.exists("{}{}_hmmsearchout".format(out,jgi_id)):
        logging.info("{} | Input {} already processed. Skipping this one...".format(cp,archive))
        return

    logging.info("{} | Running pipeline for: {} -- {}".format(cp,profile_name,archive))

    ## extract faa from archive
    ## pipe predicted genes to hmmsearch

    tar_command = ['tar', '-xOf', archive, '{}/{}.a.faa'.format(jgi_id, jgi_id)]
    tar_process = subprocess.Popen(tar_command, stdout=subprocess.PIPE)

    hmmsearch_command = get_hmmsearch_command(jgi_id,hmm,profile_name)
    hmmsearch_process = subprocess.Popen(hmmsearch_command, stdin=tar_process.stdout)#, stdout=subprocess.PIPE)

    hmmsearch_process.communicate()

    logging.info("{} | Pipeline finished for: {} -- {} | Returncode {}".format(cp,profile_name,archive,hmmsearch_process.returncode))


def get_hmmsearch_command(out_prefix,hmm,profile_name):
    docker_cmd = ['docker', 'run', '--rm', '-i', '--user', '10018:1000']
    docker_mnt = ['-v', '{}:/out'.format(out), '-v', '{}:/hmm'.format(hmm)]
    cmd = ["quay.io/biocontainers/hmmer:3.3--he1b5a44_0", 'hmmsearch',
           '-o', '/out/{}.{}.hmmsearchout'.format(profile_name,out_prefix),
           '--tblout', '/out/{}.{}.tblout'.format(profile_name,out_prefix),
           '--domtblout', '/out/{}.{}.domtblout'.format(profile_name,out_prefix),
           '-E', '0.01',
           #'--cpu', '8',
           'hmm',
           '-']

    return docker_cmd + docker_mnt + cmd




if __name__ == "__main__":

    # if hmmfile contains multiple profile it cannot read seqdb from stdin
    # since extracting is too expansive, just loop over hmm profiles

    # create a pool of workers
    logging.info("creating multiprocessing pool with {} workers...".format(processes_nr))
    pool = multiprocessing.Pool(processes=processes_nr)

    for profile in glob.glob("{}/*.hmm".format(hmms)):
        for file in glob.glob("{}/*.tar.gz".format(dir)):
            pool.apply_async(pipeline_pipes, args=(file,profile,))

    pool.close()
    pool.join()

