#!/usr/bin/env python3

import multiprocessing
import subprocess
import argparse
import re
import glob
import os
import logging
import sys


parser = argparse.ArgumentParser(description="This script predicts CRISPRs on reads")

parser.add_argument("--input", help="input directory, ncbi", required=True)
parser.add_argument("--output", help="path to output", required=True)
args = parser.parse_args()

## set up logging
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(screen_handler)

processes_nr = 10


#def get_command(r1, r2, out_prefix):
def get_command(reads, out_prefix):
    docker_cmd = ['docker', 'run', '--rm', '-i', '--user', '10018:1000']
    docker_mnt = ['-v', '{}/{}:/data'.format(args.input, out_prefix), '-v', '{}/{}:/out'.format(args.output,out_prefix)]
    tool_cmd = ["quay.io/biocontainers/crass:1.0.1--hdbcaa40_0", "crass",
                    '--outDir', 'out/',
                    '-g',
                    '--maxSpacer', '60',
                    '--maxDR', '60',
                    '--longDescription'] + reads

    return docker_cmd + docker_mnt + tool_cmd

def get_command_crisprtools(out_prefix):
    docker_cmd = ['docker', 'run', '--rm', '-i', '--user', '10018:1000']
    docker_mnt = ['-v', '{}/{}:/data'.format(args.input, out_prefix), '-v', '{}/:/out'.format(args.output)]
    tool_cmd = ["quay.io/biocontainers/crass:1.0.1--hdbcaa40_0", "crisprtools", "extract",
                    '--spacer=spacers.fasta',
                    '--direct-repeat=repeats.fasta',
                    '--flanker=flanks.fasta',
                    '--split-group',
                    '-o', '/out',
                    '--header-prefix', out_prefix+"_",
                    '/out/{}/crass.crispr'.format(out_prefix)]

    return docker_cmd + docker_mnt + tool_cmd


def run_subprocess(command):
    command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process_output, error = command_line_process.communicate()
    logging.info(error)
    return command_line_process.returncode


def make_the_call(cmd, out_prefix):
    cp = multiprocessing.current_process()
    logging.info("{} | processing {}".format(cp.name, out_prefix))
    returncode = run_subprocess(cmd)
    logging.info("{} | processing {} ... finished. Returncode {}".format(cp.name, out_prefix, returncode))


def tool(arg):
    #reads_r1 = ["/data/"+os.path.basename(x) for x in glob.glob("{}/{}/*sra_1.*_clean*".format(args.input, arg))]
    #reads_r2 = ["/data/"+os.path.basename(x) for x in glob.glob("{}/{}/*sra_2.*_clean*".format(args.input, arg))]
    reads =

    if not os.path.isdir("{}/{}".format(args.output, arg)):
        #os.mkdir(arg)
        command = get_command(reads_r1, reads_r2, arg)
        #logging.info(command)
        #make_the_call(command, arg)
    elif os.path.isfile("{}/{}/crass.crispr".format(args.output,arg)):
        logging.info("already processed. Found crispr file".format(args.output, arg))
        logging.info("extracting from crispr file...")
        command = get_command_crisprtools(arg)
        #logging.info(command)
        make_the_call(command,arg)


def multi(input):
    # create a pool of workers
    logging.info("creating multiprocessing pool with {} workers...".format(processes_nr))
    pool = multiprocessing.Pool(processes=processes_nr)
    for dir in os.listdir(input):
        pool.apply_async(tool, args=(dir,))
    pool.close()
    pool.join()


multi(args.input)

