##!/usr/bin/env python3

import multiprocessing
import subprocess
import argparse
import re
import glob
import os

parser = argparse.ArgumentParser(description="This script trims adapters and based on quality")

parser.add_argument("--input", help="input directory, ncbi", required=True)
parser.add_argument("--output", help="path to output", required=True)

args = parser.parse_args()

processes_nr = 7


def get_command(r1, r2, out_prefix):
    docker_cmd = ['docker', 'run', '--rm', '-i', '--user', '10018:1000']
    docker_mnt = ['-v', '{}/{}:/data'.format(args.input, out_prefix), '-v',
                  '{}/{}:/out'.format(args.output, out_prefix)]
    tool_cmd = ["quay.io/biocontainers/bbmap:38.86--h1296035_0", "bbduk.sh",
                'in=/data/{}'.format(r1[0]),
                'in2=/data/{}'.format(r2[0]),
                'ref=/usr/local/opt/bbmap-38.86-0/resources/adapters.fa',
                'qtrim=r',
                'trimq=10',
                'ftm=5',
                'out=/out/{}_clean.fastq.gz'.format(r1[0]),
                'out2=/out/{}_clean.fastq.gz'.format(r2[0]),
                'stats=/out/{}_stats'.format(r1[0])]

    return docker_cmd + docker_mnt + tool_cmd


def get_assembly_command(sra,sra_id):
    return ['fastq-dump', '--stdout', sra, '|', 'tools/src/bbmap/bbduk.sh', 'in=stdin.fastq',
            'int=t', 'ref=/tools/src/bbmap/resources/adapters.fa', 'qtrim=r', 'trimq=10', 'ftm=5', 'out=stdout.fq',
            '-minlength=21', '|', 'docker', 'run', '--rm', '--user', '10018:1000', '-v',
            '/data/tobias/metagenomes/geotraces/reads/:/data', '-v', '/data/tobias/geotraces_asssemblies/:/out',
            'c3fd4c1b9681', 'megahit', '-12', 'stdin', '-t', '24', '--k-min', '21', '--k-max' '141', '--k-step' '10',
            '--bubble-level', '1', '--prune-level', '1', '--cleaning-rounds', '5', '-o', '{}_megahit_out'.format(sra_id)]


def run_subprocess(command):
    command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process_output, _ = command_line_process.communicate()
    # print(process_output)
    return command_line_process.returncode


def make_the_call(cmd, out_prefix):
    cp = multiprocessing.current_process()
    print("{} | processing {}".format(cp.name, out_prefix))
    returncode = run_subprocess(cmd)
    print("{} | processing {} ... finished. Returncode {} | time: {}".format(cp.name, out_prefix, returncode))


def tool(arg):
    # reads_r1 = [os.path.basename(x) for x in sorted(glob.glob("{}/{}/*sra_1*".format(args.input, arg)))]
    # reads_r2 = [os.path.basename(x) for x in sorted(glob.glob("{}/{}/*sra_2*".format(args.input, arg)))]
    #sra = [os.path.basename(x) for x in sorted(glob.glob("{}/*.sra".format(args.input)))]
    sra_id = os.path.basename(arg).split(".")[0]

    #os.mkdir(arg)

    # command = get_command(sra)
    command = get_assembly_command(arg,sra_id)
    print(command)
    make_the_call(command, arg)


def multi(input):
    # create a pool of workers
    print("creating multiprocessing pool with {} workers...".format(processes_nr))
    pool = multiprocessing.Pool(processes=processes_nr)
    # for file in glob.glob("{}/*.fna".format(dir)):
    for file in glob.glob("{}/*.sra".format(dir)):
        # for dir in os.listdir(input):
        pool.apply_async(tool, args=(dir,))
    pool.close()
    pool.join()


multi(args.input)
