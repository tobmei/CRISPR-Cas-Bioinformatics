#!/usr/bin/env python3

import multiprocessing
import subprocess
import argparse
import re
import glob
import time


parser = argparse.ArgumentParser(description="This script does the following...")

parser.add_argument("--input", help="input directory", required=True)
parser.add_argument("--output", help="path to output", required=True)

args = parser.parse_args()

dir = args.input
out = args.output

processes_nr = 16



def get_command(file, out_prefix):
    docker_cmd = ['docker', 'run', '--rm', '-i', '--user', '10018:100']
    docker_mnt = ['-v', '{}:/contigs.fa'.format(file), '-v', '{}:/out'.format(out)]
    prodigal_cmd = ["quay.io/biocontainers/prodigal:2.6.3--h516909a_2", 'prodigal',
                    '-i', 'contigs.fa',
                    #'-o', '/out/{}_coords.gbk'.format(out_prefix),
                    '-a', '/out/{}_proteins.faa'.format(out_prefix),
                    '-p', 'meta']

    return docker_cmd + docker_mnt + prodigal_cmd


def run_subprocess(command):
    start = time.process_time()
    command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process_output, _ = command_line_process.communicate()
    #print(process_output)
    elapsed = time.process_time() - start
    return command_line_process.returncode, round(elapsed, 2)


def make_the_call(cmd, out_prefix, processed):
    cp = multiprocessing.current_process()
    print("{} | processing file: {}".format(cp.name, out_prefix))
    returncode, elapsed = run_subprocess(cmd)
    print("{} | processing file {} ... finished. Returncode {} | time: {}".format(cp.name, out_prefix, returncode, elapsed))


def prodigal(file):
    out_prefix = re.search(re.compile(".*\/(33.*)\.a\.fna"),file).group(1)
    command = get_command(file, out_prefix)
    make_the_call(command, out_prefix, processed)


def multi(dir):
    # create a pool of workers
    print("creating multiprocessing pool with {} workers...".format(processes_nr))
    pool = multiprocessing.Pool(processes=processes_nr)
    for file in glob.glob("{}/*.fna".format(dir)):
        pool.apply_async(prodigal, args=(file,))
    pool.close()
    pool.join()


processed = 0
multi(dir)

