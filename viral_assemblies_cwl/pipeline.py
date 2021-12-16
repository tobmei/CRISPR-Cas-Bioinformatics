#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 13:57:47 2019

@author: tobias
"""

import argparse
import os
import re
import subprocess
import time
import multiprocessing
import logging
import sys


parser = argparse.ArgumentParser(description="this script does the following...")

#parser.add_argument('--jobdir', help="path to directory with job files", required=True)
parser.add_argument("--output", help="output directory", required=True)
parser.add_argument('--machine', help="name of machine to run", required=True)
parser.add_argument('--forward',help="forward reads",required=True)
parser.add_argument('--reverse',help="reverse reads",required=True)
parser.add_argument('--ALE',help="only run ALE workflow", default=False, action='store_true')
parser.add_argument('--jobfiles',help="list of job files", nargs='+')#type=argparse.FileType('r')

args = parser.parse_args()


# logging.basicConfig(filename="pipeline.log",
#                     level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(message)s')



#Assuming job files named job_<assembler>_<nr>.yml
output = args.output
tmpdir_prefix = "tmeiercwl"
machine = args.machine
forward_reads = args.forward
reverse_reads = args.reverse
jobfiles = args.jobfiles
just_ale = args.ALE

job_pattern = re.compile("job_(.*)_(\d*)")

kmin_pattern = re.compile("kmin: ([0-9]*)")
kmax_pattern = re.compile("kmax: ([0-9]*)")
kstep_pattern = re.compile("kstep: ([0-9]*)")
bubble_pattern = re.compile("megaNoBubble: (.*)")
klist_pattern = re.compile("kList: (.*)")
rr_pattern = re.compile("(disableRR: .*)")


nr_jobs = len(jobfiles)
processes_nr = 0
cpu_nr = 0
threads = 0
if machine == "ford":
    threads = 56
    cpu_nr = 14
    processes_nr = 4
if machine == "newton":
    threads = 176
    cpu_nr = 8
    processes_nr = 22


bbmap_docker = "bryce911/bbtools"
reformat_call = "/tools/src/bbmap/reformat.sh"
megahit_docker = "quay.io/biocontainers/megahit:1.1.3--py35_0"
metaspades_docker = "quay.io/biocontainers/spades:3.13.0--0"
idbaud_docker = "myidba"
ale_docker = "quay.io/biocontainers/ale:20180904--py27ha92aebf_0"
kraken_docker = "quay.io/biocontainers/kraken2:2.0.7_beta--pl526h6bb024c_3"
diamond_docker = "quay.io/biocontainers/diamond:0.9.26--hfb76ee0_0"
virsorter_docker = "simroux/virsorter:v1.0.5"
virsorter_run = "/data/tobias/virsorter-data"
mycc_docker = "990210oliver/mycc.docker:v1"

kraken2db = "krakendb_novirus"
diamonddb = "diamonddb_IMGVIR.dmnd"

result_list = []
docker_cmd = ['docker','run','--rm','-i','--user','10018:100']
docker_mnt = ['-v','/data/tobias/tmp:/work/tmp',\
              '-v','{}:/work/outdir'.format(output),\
              '-v',"{}:/data/forward.fastq".format(forward_reads),\
              '-v',"{}:/data/reverse.fastq".format(reverse_reads),\
              '-v',"/data/tobias/databases/:/databases/"]

#if not os.path.exists(jobdir_path):
#    sys.exit("jobdir path {} not found".format(jobdir_path))

#create output directory
#if not os.path.exists(output):
#    os.system("mkdir {}".format(output))

def get_params(job_file):
    f = open(job_file,"r")
    contents = f.read()
    kmin=kstep=kmax=bubble=rr=klist = ''
    if kmin_pattern.match(contents):
        kmin = kmin_pattern.search(contents).group(1)
    if kstep_pattern.match(contents):
        kstep = kstep_pattern.search(contents).group(1)
    if kmax_pattern.match(contents):
        kmax = kmax_pattern.search(contents).group(1)
    if bubble_pattern.match(contents):
        bubble = bubble_pattern.search(contents).group(1)
    if rr_pattern.match(contents):
        rr = rr_pattern.search(contents).group(1)
    if klist_pattern.match(contents):
        klist = klist_pattern.search(contents).group(1)
    f.close()
    return [kmin,kstep,kmax,bubble,klist,rr]


def get_megahit_cmd(kmin,kstep,kmax,job_nr,bubble):

    docker_mnt = ['-v','/data/tobias/tmp:/work/tmp',\
                  '-v','{}:/work/outdir'.format(output),\
                  '-v',"{}:/data/forward.fastq".format(forward_reads),\
                  '-v',"{}:/data/reverse.fastq".format(reverse_reads)]

    megahit_cmd = [megahit_docker,'megahit',\
                   '-1','/data/forward.fastq'.format(job_nr),\
                   '-2','/data/reverse.fastq'.format(job_nr),\
                   '--tmp-dir','/work/tmp',\
                   '--k-min',kmin,\
                   '--k-max',kmax,\
                   '--k-step',kstep,\
                   '--bubble-level',bubble,\
                   '-o','/work/outdir/{}/megahit'.format(job_nr),\
                   '-t',str(cpu_nr)]

    return docker_cmd + docker_mnt + megahit_cmd

def get_metaspades_cmd(job_nr,klist,rr):

    docker_mnt = ['-v','{}:/work/outdir'.format(output),\
                  '-v',"{}:/data/forward.fastq".format(forward_reads),\
                  '-v',"{}:/data/reverse.fastq".format(reverse_reads)]

    metaspades_cmd = [metaspades_docker, 'spades.py',\
                      '-t',str(cpu_nr),\
                      '--meta',\
                      '-o','/work/outdir/{}/metaspades'.format(job_nr),\
                      '-1','/data/forward.fastq'.format(job_nr),\
                      '-2','/data/reverse.fastq'.format(job_nr),\
                      '-k',klist]
#                      '--disable-rr',rr]

    return docker_cmd + docker_mnt + metaspades_cmd


def get_bbmap_cmd(job_nr,assembler,contig_file):

    docker_mnt = ['-v','{}:/work/outdir'.format(output),\
                  '-v',"{}:/data/forward.fastq".format(forward_reads),\
                  '-v',"{}:/data/reverse.fastq".format(reverse_reads)]

    bbmap_cmd = [bbmap_docker,'bbmap.sh',\
                 'in=/data/forward.fastq',\
                 'in2=/data/reverse.fastq',\
                 'ref=/work/outdir/{}/{}/{}'.format(job_nr,assembler,contig_file),\
                 '-Xmx30g',\
                 't={}'.format(cpu_nr),\
                 'nodisk=t',\
                 'out=/work/outdir/{}/mapping.bam'.format(job_nr),\
                 'statsfile=/work/outdir/{}/bbmap.stats'.format(job_nr),\
                 'covstats=/work/outdir/{}/bbmap.covstats'.format(job_nr),\
                 'covhist=/work/outdir/{}/bbmap.covhist'.format(job_nr),\
                 'bincov=/work/outdir/{}/bbmap.bincov'.format(job_nr)]

    return docker_cmd + docker_mnt + bbmap_cmd


def get_samtools_cmd(output,job_nr):

    sort_cmd = ['samtools','sort',\
                 '-@',str(cpu_nr),\
                 '-O','BAM',\
                 '-o','{}/{}/sorted.bam'.format(output,job_nr),\
                 '{}/{}/mapping.bam'.format(output,job_nr)]

    return sort_cmd


def get_ale_cmd(job_nr,assembler,contig_file):

    docker_mnt = ['-v','{}:/work/outdir'.format(output)]

    ale_cmd = [ale_docker,'ALE',\
               '--metagenome',\
               '--nout',\
               '/work/outdir/{}/sorted.bam'.format(job_nr),\
               '/work/outdir/{}/{}/{}'.format(job_nr,assembler,contig_file),\
               '/work/outdir/{}/ALEoutput.txt'.format(job_nr)]

    return docker_cmd + docker_mnt + ale_cmd

def get_kraken2_cmd(job_nr):

    docker_mnt = ['-v','{}:/work/outdir'.format(output),\
                  '-v',"{}:/data/forward.fastq".format(forward_reads),\
                  '-v',"{}:/data/reverse.fastq".format(reverse_reads),\
                  '-v',"/data/tobias/databases/:/databases/"]

    kraken_cmd = [kraken_docker, 'kraken2',\
                  '--db','/databases/{}'.format(kraken2db),\
                  '--threads',str(cpu_nr),\
                  '--paired',\
#                  '--confidence','0.1',\
                  '--unclassified-out', '/work/outdir/{}/useqs#.fastq'.format(job_nr),\
                  '--classified-out', '/work/outdir/{}/cseqs#.fastq'.format(job_nr),\
                  '--output', '/work/outdir/{}/kraken.output.txt'.format(job_nr),\
                  '--report', '/work/outdir/{}/kraken.report.txt'.format(job_nr),\
                  '/data/forward.fastq',\
                  '/data/reverse.fastq']

    return docker_cmd + docker_mnt + kraken_cmd


def get_diamond_cmd(job_nr,assembler):

    docker_mnt = ['-v','{}:/work/outdir'.format(output),\
                  '-v',"/data/tobias/databases/:/databases/"]

    diamond_cmd = [diamond_docker, 'diamond', 'blastx',\
                   '--out', '/work/outdir/{}/diamond.matches.tsv'.format(job_nr),\
                   '--outfmt', '6',\
                   '--threads', str(cpu_nr),\
                   '--sensitive',\
                   '--quiet',\
                   '--query', '/work/outdir/{}/{}/final.contigs.fa'.format(job_nr,assembler),\
                   '--db', '/databases/{}'.format(diamonddb)]

    return docker_cmd + docker_mnt + diamond_cmd


def get_virsorter_cmd(job_nr,assembler,cur_job_dir):

    docker_mnt = ['-v','{}:/work/outdir'.format(output),\
                  '-v','/data/tobias/virsorter-data:/data',\
                  '-v','{}:/wdir'.format(cur_job_dir),\
                  '-w','/wdir',\
                  '-v',"/data/tobias/databases/:/databases/"]

    virsorter_cmd = [virsorter_docker,\
                     '--db', '2',\
                     '--virome',\
                     '--diamond',\
                     '--ncpu', str(cpu_nr),\
                     '--fna', '/work/outdir/{}/{}/final.contigs.fa'.format(job_nr,assembler)]

    return docker_cmd + docker_mnt + virsorter_cmd

def create_depth_file(cur_job_dir):

    tail = subprocess.Popen(['tail','-n','+4','{}/bbmap.bincov'.format(cur_job_dir)], stdout=subprocess.PIPE)
    cut = subprocess.Popen(['cut -f1,2 - > {}/mycc.depth.txt'.format(cur_job_dir)], stdin=tail.stdout, shell=True)
    returncode = cut.communicate()[0]

    return returncode


def run_subprocess(command):

    command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    process_output, _ =  command_line_process.communicate()

    logging.info(command)
    logging.info(process_output)

    return command_line_process.returncode


def get_mycc_cmd(job_nr,cur_job_dir,assembler,contig_file):

    docker_mnt = ['-v','{}:/work/outdir'.format(output)]

    mycc_cmd = [mycc_docker,'MyCC.py',\
                '/work/outdir/{}/{}/{}'.format(job_nr,assembler,contig_file),\
                '-meta',\
                '-a','work/outdir/{}/mycc.depth.txt'.format(job_nr)]

    return docker_cmd + docker_mnt + mycc_cmd

def make_the_call(step,cmd,job_nr):

    cp = multiprocessing.current_process()

    print("{} | job {} | running {} ...".format(cp.name,job_nr,step))
    returncode = run_subprocess(cmd)
    print("{} | job {} | running {} ... finished. Returncode {}".format(cp.name,job_nr,step,returncode))


def assembly(job_file):

    assembler = job_pattern.search(job_file).group(1)
    job_nr = job_pattern.search(job_file).group(2)
    cur_job_dir = "{}/{}/".format(output,job_nr)

    if assembler == "megahit":
        contig_file = "final.contigs.fa"
    else:
        contig_file = "contigs.fasta"

#    #create job output directory
#    if not os.path.exists(assembler_dir): #output/megahit?
#        os.system("mkdir {}".format(assembler_dir))

    # megahit has to create the output directory --> megahit/job_nr
    if not os.path.exists(cur_job_dir):
        os.system("mkdir {}".format(cur_job_dir)) #ouput/1

    #get parameter from job file
    kmin,kstep,kmax,bubble,klist,rr = get_params(job_file)
#    print(kmin+","+kstep+","+kmax+","+bubble+","+klist+","+rr)

    ### run the steps of the pipeline ###
#    kraken_cmd = get_kraken2_cmd(job_nr)
#    make_the_call("kraken2",kraken_cmd,job_nr)

#    megahit_cmd = get_megahit_cmd(kmin,kstep,kmax,job_nr,bubble)
#    make_the_call("megahit",megahit_cmd,job_nr)

    metaspades_cmd = get_metaspades_cmd(job_nr,klist,rr)
    make_the_call("metaspades",metaspades_cmd,job_nr)

    bbmap_cmd = get_bbmap_cmd(job_nr,assembler,contig_file)
    make_the_call("bbmap",bbmap_cmd,job_nr)

    samtools_cmd = get_samtools_cmd(output,job_nr)
    make_the_call("samtools sort",samtools_cmd,job_nr)

    ale_cmd = get_ale_cmd(job_nr,assembler,contig_file)
    make_the_call("ALE",ale_cmd,job_nr)
#
#    diamond_cmd = get_diamond_cmd(job_nr,assembler)
#    make_the_call("diamond",diamond_cmd,job_nr)
#
#    virsorter_cmd = get_virsorter_cmd(job_nr,assembler,cur_job_dir)
#    make_the_call("virsorter",virsorter_cmd,job_nr)

#    create_depth_file(cur_job_dir)

#    mycc_cmd = get_mycc_cmd(job_nr,cur_job_dir,assembler)
#    make_the_call("mycc",mycc_cmd,job_nr)


#
def multi(jobs):
    #create a pool of workers
    print("creating multiprocessing pool with {} workers...".format(processes_nr))
    pool = multiprocessing.Pool(processes=processes_nr)
    for file in jobs:
        pool.apply_async(assembly, args=(file,))
    pool.close()
    pool.join()

multi(jobfiles)

#assembly(jobfiles[1])

#docker run --rm -it --user 10018:100 -v /data/MeDaMCAn/datasets/Bioreaktor/:/data/ virusx/bbmap:36.84--0 bbduk2.sh stats=bbduk.stats out1=/data/vDNA_clean1.fastq out2=/data/vDNA_clean2.fastq outm=/data/vDNA_matched1.fastq outm2=/data/vDNA_matched2.fastq rref=/usr/local/opt/bbmap-36.84/resources/adapters.fa entropy=0.5 entropywindow=35 minlength=35 k=27 mink=8 forcetrimmod=5 hdist=1 in=/data/BGR_vDNA_viral_S0_L000_R1_000_val_1.fastq.gz in2=BGR_vDNA_viral_S0_L000_R2_000_val_2.fastq.gz


