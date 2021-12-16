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
    description="This script calls multiple instances of CRISPRCasFinder")

parser.add_argument("--metagenomes", help="input jgi metagenomes (i.e. gzipped tar archives)", nargs='+', required=True)
parser.add_argument("--output", help="path to output folder", required=True)
parser.add_argument("--workers", help="number of parallel processes", type=int, required=True)
#parser.add_argument("--mcpu", help="number of cpus used for Mycisfinder(?)", required=True)

args = parser.parse_args()
metagenomes = args.metagenomes
output_dir = args.output
workers = args.workers
#mcpu = args.mcpu

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#handler = logging.FileHandler('log.txt', mode='w')
#handler.setFormatter(formatter)
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#logger.addHandler(handler)
logger.addHandler(screen_handler)

# name of docker image on newton and ford
crisprcasfinder = "crisprcasfinder"


def call_subprocess(command, cp):
    #logging.debug("{} | {}".format(cp.name, command))
    command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    process_output, stderr = command_line_process.communicate()
    logging.debug("{} | Error: {}".format(cp.name, stderr))

    return command_line_process.returncode


def analysis(metagenome):
    cp = multiprocessing.current_process()
    ## get sample id
    sample_id = re.match(re.compile(r".*/([0-9]*)\.tar\.gz$"), metagenome).group(1)

    ## extract contigs (*.a.fna) from tar archive to output folder
    logging.info("{} |untar contig file from {}".format(cp.name, metagenome))
    untar_contigs = ["tar", "-C", output_dir, "-xzf", metagenome, "{}/{}.a.fna".format(sample_id, sample_id)]
    returncode_untar = call_subprocess(untar_contigs, cp)
    logging.info("{} | Finished untar: {}".format(cp.name, returncode_untar))
    contig_file = "{}{}/{}.a.fna".format(output_dir, sample_id, sample_id)

    ## run CRISPRCasFinder on contigs
    docker_cmd = ['docker', 'run', '--rm', #'--user', '10018:100',
                  '-v', "{}:/data/contigs.fna".format(contig_file),
                  '-v', "{}:/output".format(output_dir),
                  crisprcasfinder, 'CRISPRCasFinder.pl',
                  '-in', '/data/contigs.fna',
                  '-so', '/opt/CRISPRCasFinder-release-4.2.19/sel392v2.so',
                  '-out', '/output/{}_result'.format(sample_id),
                  #'-cas',
                  #'-def', 'SubTyping',
                  #'-cpuM', mcpu,
                  #'-meta',
                  '-quiet']

    logging.info("{} | Running CRISPRCasFinder on {}".format(cp.name, contig_file))
    returncode_finder = call_subprocess(docker_cmd, cp)
    logging.info("{} | CRISPRCasFinder finished on {}: {}".format(cp.name, contig_file, returncode_finder))

    ## remove extracted contig file
    logging.info("{} | Removing extracted folder: {}".format(cp.name, sample_id))
    rm_contigs = ["rm", "-r", "{}{}".format(output_dir,sample_id)]
    call_subprocess(rm_contigs, cp)


if __name__ == "__main__":

    # create a pool of workers
    logging.info("creating multiprocessing pool with {} workers...".format(workers))
    pool = multiprocessing.Pool(processes=workers)
    for metagenome in metagenomes:  ## 'metagenome' == jgt tar archive (3330000123.tar.gz)
        pool.apply_async(analysis, args=(metagenome,))
    pool.close()
    pool.join()
