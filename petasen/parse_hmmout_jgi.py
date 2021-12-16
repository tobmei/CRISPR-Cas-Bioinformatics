#!/usr/bin/env python3

import argparse
import re
import glob
import subprocess
import multiprocessing
import logging
import tarfile
import sys
from Bio import SeqIO
from Bio import SearchIO
import os

parser = argparse.ArgumentParser(description="This script parses the output of hmmsearch for multiple jgi metagenomes")

parser.add_argument("--input", help="path to input files (i.e. hmmsearch output)", required=True)
parser.add_argument("--jgi_input", help="path to jgi archives", required=True)

args = parser.parse_args()
hmmout_path = args.input
jgi_path = args.jgi_input

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# handler = logging.FileHandler('log.txt', mode='w')
# handler.setFormatter(formatter)
screen_handler = logging.StreamHandler(stream=sys.stderr)
screen_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# logger.addHandler(handler)
logger.addHandler(screen_handler)


def get_tax_for_targets(sign_hits_dict, jgi_id):

    archive = ("{}/{}.tar.gz".format(jgi_path,jgi_id))
    phylodist_exists = False
    config_exists = False

    # check if files phylodist and config are present in archive
    tar = subprocess.Popen(['tar', '-tf', archive], stdout=subprocess.PIPE)
    grep = subprocess.Popen(['grep', '-e', '{}/{}.a.phylodist.txt'.format(jgi_id, jgi_id), '-e', '{}/{}.config'.format(jgi_id,jgi_id)],
                            stdin=tar.stdout,stdout=subprocess.PIPE)
    stdout, _ = grep.communicate()
    if len(stdout) > 0:  # grep found something
        # convert to string and split. Gives ['file1','file2']
        stdout = stdout.decode("utf-8").strip().split("\n") # stdout gives bytearray. decode to string
        if len(stdout) == 2: # 2 files found
            phylodist_exists, config_exists = True, True
        else: # only one file found. Which?
            if re.match(r'.*config', stdout[0]):
                config_exists = True
            elif re.match(r'.*phylodist.txt', stdout[0]):
                phylodist_exists = True

    # get taxonomic annotation
    if phylodist_exists:
        # build up grep command. Add targets as regex
        grep_cmd = ['grep', '-w']  # -w -> only exact matches
        for target, _ in sign_hits_dict.items():
            grep_cmd.append('-e')
            grep_cmd.append(target)


        tar_command = ['tar', '-xOf', archive, '{}/{}.a.phylodist.txt'.format(jgi_id, jgi_id)]
        tar_process = subprocess.Popen(tar_command, stdout=subprocess.PIPE)
        grep_process = subprocess.Popen(grep_cmd, stdin=tar_process.stdout, stdout=subprocess.PIPE) # stdout=PIPE necessary to get output with communicate()
        stdout, stderr = grep_process.communicate()
        if len(stdout) > 0:  # grep found someting
            stdout = stdout.decode("utf-8").strip().split("\n")  # gives me a list of hits
            # for each hit, get the lineage
            for hit in stdout:
                hit = hit.split("\t")
                target_name = hit[0]
                #percent_identity = hit[3]
                lineage = hit[4].split(";")
                k = "NA" if len(lineage) < 1 else lineage[0]
                p = "NA" if len(lineage) < 2 else lineage[1]
                c = "NA" if len(lineage) < 3 else lineage[2]
                o = "NA" if len(lineage) < 4 else lineage[3]
                f = "NA" if len(lineage) < 5 else lineage[4]
                g = "NA" if len(lineage) < 6 else lineage[5]
                s = "NA" if len(lineage) < 7 else lineage[6]
                st = "NA" if len(lineage) < 8 else lineage[7]
                # add lineage to dictionary
                #sign_hits_dict[target_name]['percent_identity'] = percent_identity
                sign_hits_dict[target_name]['k'] = k
                sign_hits_dict[target_name]['p'] = p
                sign_hits_dict[target_name]['c'] = c
                sign_hits_dict[target_name]['o'] = o
                sign_hits_dict[target_name]['f'] = f
                sign_hits_dict[target_name]['g'] = g
                sign_hits_dict[target_name]['s'] = s
                sign_hits_dict[target_name]['st'] = st

    # extract environmental meta data for the sample
    if config_exists:
        tar_command = ['tar', '-xOf', archive, '{}/{}.config'.format(jgi_id, jgi_id)]
        tar_process = subprocess.Popen(tar_command, stdout=subprocess.PIPE)
        grep_process = subprocess.Popen(['grep', '-e', 'ir_class', '-e', 'ir_order'], stdin=tar_process.stdout, stdout=subprocess.PIPE)
        stdout, stderr = grep_process.communicate()
        if len(stdout) > 0:  #grep found something
            stdout = stdout.decode("utf-8").strip().split("\n")
            if len(stdout) == 2:
                ir_class = stdout[0].split(" ",1)[1]
                ir_order = stdout[1].split(" ",1)[1]
            else:  # only one feature found. Which?
                if re.match(r'.*class', stdout[0]):
                    ir_class = stdout[0].split(" ",1)[1]
                    ir_order = "NA"
                elif re.match(r'.*order', stdout[0]):
                    ir_order = stdout[0].split(" ",1)[1]
                    ir_class = "NA"
    else:
        ir_class = "NA"
        ir_order = "NA"

    return sign_hits_dict, ir_class, ir_order




def parse_hmmsearch_output(hmm_output_file, jgi_id):
    cp = multiprocessing.current_process().name
    logging.info("{} | ####Processing#### {}".format(cp,hmm_output_file))

    sign_hits_dict = {}
    found_hits = False

    with open(hmm_output_file, "r") as inp:
        for line in inp:
            if line.startswith("#"):
                continue

            l = line.split()
            target_name = l[0]
            query_name = l[2]
            evalue = l[4]
            score = l[5]
            bias = l[6]
            bestdom_evalue = l[7]
            bestdom_score = l[8]
            bestdom_bias = l[9]
            exp_dom_nr = l[10]

            if float(score) >= 70.0: # bitscore is highly significant
                found_hits = True
                if target_name not in sign_hits_dict:
                    sign_hits_dict[target_name] = {}
                sign_hits_dict[target_name]['evalue'] = evalue
                sign_hits_dict[target_name]['score'] = score
                sign_hits_dict[target_name]['bias'] = bias
                sign_hits_dict[target_name]['dom_nr'] = exp_dom_nr
                sign_hits_dict[target_name]['bestdom_evalue'] = bestdom_evalue
                sign_hits_dict[target_name]['bestdom_score'] = bestdom_score
                sign_hits_dict[target_name]['bestdom_bias'] = bestdom_bias

    # get taxonomic annotation for hit from phylodist file
    if found_hits:
        sign_hits_dict, ir_class, ir_order = get_tax_for_targets(sign_hits_dict, jgi_id)
        # write to stdout
        for target, values in sign_hits_dict.items():
                print(jgi_id+"\t"+ir_class+"\t"+ir_order+"\t"+target+"\t"+query_name+"\t"+values['evalue']+"\t"+values['score']+"\t"+values['bias']+"\t"+
                      values['k']+"\t"+values['p']+"\t"+values['c']+"\t"+values['o']+"\t"+values['f']+"\t"+values['g']+"\t"+values['s']+"\t"+values['st'])


    logging.info("{} | ####Finished#### {}".format(cp,hmm_output_file))

    #get the sequence
    #index = SeqIO.index("/data/tobias/algae_metagenomes/{}_proteins.faa".format(sample),"fasta")
    #sequence = index.get(target_name).seq
    #print(sequence)


if __name__ == "__main__":

    processes_nr = 100
    # processed_ids = open(already_processed_file, "r").read()
    pattern = "^.*(33000[0-9]+)\..*"
    hmm_tblout_files = [x for x in glob.glob("{}/*.tblout".format(hmmout_path))]

    print("jgi_id\tenvironment_class\tenvironment_order\ttarget\tquery\te-value\tbitscore\tbias\tkingdom\tphylum\tclass\torder\tfamily\tgenus\tspecies\tstrain")


    # create a pool of workers
    pool = multiprocessing.Pool(processes=processes_nr)
    for file in hmm_tblout_files:
        jgi_id = re.compile(pattern).search(file).group(1)
        pool.apply_async(parse_hmmsearch_output, args=(file,jgi_id,))
    pool.close()
    pool.join()
