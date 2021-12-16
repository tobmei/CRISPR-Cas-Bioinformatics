#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 12:08:40 2019

@author: tobias
"""

import argparse
import glob
import re
import os

parser = argparse.ArgumentParser(description="this script does the following...")

parser.add_argument('--input', help="path to input directory ", required=True)
parser.add_argument('--jobfiles',help="list of job files", nargs='+',required=True)


args = parser.parse_args()

input_dir = args.input
jobfiles = args.jobfiles

first = True #flag for writing onyl one header line to output

job_pattern = re.compile(".*job_(.*)_(.*).yml")
ALE_score = re.compile("# ALE_score: (.*)")
ALE_cov = re.compile("# depthAvg: (.*)")
ALE_reads = re.compile("# totalReads: (.*)")
ALE_mapped = re.compile("# totalMappedReads: (.*)")
kmin_pattern = re.compile(".*kmin: ([0-9]*)")
kmax_pattern = re.compile(".*kmax: ([0-9]*)")
kstep_pattern = re.compile(".*kstep: ([0-9]*)")
bubble_pattern = re.compile("megaNoBubble: (.*)")

ale_file = "ALEoutput.txt"



def add_to_statsfile(assembler,job_nr,score,cov,mapped,kmin,kmax,kstep,bubble):
    with open("{}/assembly_stats.txt".format(input_dir),"r") as inp:
        with open ("{}/assembly_stats_mod.txt".format(input_dir),"a") as outp:
            for line in inp:
                #get correct line i.e. that matches job_nr and assembler
                split = line.split("\t")[10] #gets last field

                if first:
                    if re.match(r"filename",split): #write header
                        line = line.strip("\n") + "\tassembler\tjob_nr\tale_score\tkmin\tkmax\tkstep\tbubble\tavg_cov\tperc_mapped\n"
                        print(line,file=outp)

                if re.match(r".*\/{}\/{}\/.*$".format(job_nr,assembler), split):
                    line = line.strip("\n") + "\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(assembler,job_nr,score,kmin,kmax,kstep,bubble,cov,mapped)
                    print(line,file=outp)






def get_ALE(ale_file):
    f = open(ale_file,"r")
    contents = f.read()
    score = ALE_score.search(contents).group(1)
    cov = ALE_cov.search(contents).group(1)
    reads = float(ALE_reads.search(contents).group(1))
    mapped = float(ALE_mapped.search(contents).group(1))
    perc_mapped = str(round((mapped/reads)*100,2))
    f.close()

    return [score,cov,perc_mapped]

def get_ks(job_file):
    f = open(job_file,"r")
    contents = f.read()
    kmin = kmin_pattern.search(contents).group(1)
    kstep = kstep_pattern.search(contents).group(1)
    kmax = kmax_pattern.search(contents).group(1)
    bubble = '0'#bubble_pattern.search(contents).group(1)
    f.close()
    return [kmin,kmax,kstep,bubble]

for job in jobfiles:
    assembler = job_pattern.search(job).group(1)
    job_nr = job_pattern.search(job).group(2)
    kmin,kmax,kstep,bubble = get_ks(job)

    score,cov,mapped = get_ALE("{}/{}/{}".format(input_dir,job_nr,ale_file))

    add_to_statsfile(assembler,job_nr,score,cov,mapped,kmin,kmax,kstep,bubble)

    first = False











