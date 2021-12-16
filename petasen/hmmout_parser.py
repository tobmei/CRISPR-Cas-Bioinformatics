#!/usr/bin/env python3

import argparse
import re
import glob
from Bio import SeqIO
from Bio import SearchIO
import os

parser = argparse.ArgumentParser(description="This script parses the output of hmmsearch")

parser.add_argument("--input", help="path to input files (i.e. hmmsearch output)", required=True)
parser.add_argument("--bin_to_tax", help="file with bin to taxonomy mapping", required=False)
parser.add_argument("--sample_to_health", help="file with sample to health mapping", required=False)

args = parser.parse_args()
dir_in = args.input
bin_to_tax = args.bin_to_tax
sample_to_health = args.sample_to_health

#pattern for mags proteins
#pattern = ".*(.RR.*_bin\.[0-9]+).*"

#pattern for umgs proteins
#pattern = "^.*(S[0-9]*)_.*"

#pattern for jgi data
pattern = "^.*(33[0-9]*)_.*"

# dictionary to store significant hits while parsing the files
sign_hits_dict = {}
# dictionary to store sample meta data
meta_dict = {}


def print_dictionaries():
    # print header
    print("sample,target,evalue,score,bias,dom_nr,bestdom_evalue,bestdom_score,bestdom_bias,kingdom,phylum,class,order,family,genus,species")
    for smpl, hits in sign_hits_dict.items():
        for target, stats in hits.items():
            print(smpl + "," + target + ",", end="")  # dont print newline (python 3.7)
            #print(smpl + "," + target + ","),  # comma means: dont print newline (python 2)
            #for val in stats.values():
            print(stats['evalue']+","+stats['score']+","+stats['bias']+","+stats['dom_nr']+","+stats['bestdom_evalue']+
                  ","+stats['bestdom_score']+","+stats['bestdom_bias'])
            #if meta_dict.__contains__(smpl):
                #print(meta_dict[smpl]['kingdom']+","+meta_dict[smpl]['phylum']+","+meta_dict[smpl]['class']+","+meta_dict[smpl]['order']+
                      #","+meta_dict[smpl]['family']+","+meta_dict[smpl]['genus']+","+meta_dict[smpl]['species'])
            #else:
                #print("NA,NA,NA,NA,NA,NA,NA")

def print_fasta():
    for smpl, hits in sign_hits_dict.items():
        for target, stats in hits.items():
            print(">"+smpl + "|" + target)
            # for val in stats.values():
            print(stats['sequence'])


# get significant hits from *_tblout files inside path
# for each sample with significant hits, get metadata for sample (taxonomy and health)
# look for sample ID in bin_to_tax and bin_to_health
# first parse bin_to_tax and save data in dictionary
# dont parse it for evry entry
# data_dict = {sampleID: {sign hit: {key:value, key:value}, sign hit: {...} }, sampleID: {...}, ...}

def parse_hmmsearch_output():
    for file in glob.glob("{}/*_tblout".format(dir_in)):
        # sample = re.compile(".*(UMGS[0-9]+)_*").search(file).group(1) # human gut umgs
        # extract sample ID from file name
        sample = re.compile(pattern).search(file).group(1)
        #hmm_result = SearchIO.read(file, "hmmsearch3-domtab")


        with open(file, "r") as inp:
            for line in inp:
                entry_is_significant = False
                if not line.startswith("#"):
                    #gc_content = re.compile(".*gc_cont=(.*)$").search(line).group(1)
                    l = line.split()
                    target_name = l[0]
                    evalue = l[4]
                    score = l[5]
                    bias = l[6]
                    bestdom_evalue = l[7]
                    bestdom_score = l[8]
                    bestdom_bias = l[9]
                    dom_nr = l[11]

                    if float(score) >= 50.0:  # filter based on evalue
                        entry_is_significant = True

                if entry_is_significant:
                    #copy file to different folder
                    #os.system("cp {}/{}_proteins.faa_hmmsearchout ../hmm_sign".format(dir_in,sample))
                    if not sign_hits_dict.__contains__(sample):
                        #if hit is significant, write sample ID to dictionary and initialize empty dict
                        sign_hits_dict[sample] = {}
                        #meta_dict[sample] = {}
                        #get the sequence
                        #index = SeqIO.index("/data/tobias/algae_metagenomes/{}_proteins.faa".format(sample),"fasta")
                        #sequence = index.get(target_name).seq
                        #print(sequence)

                    sign_hits_dict[sample][target_name] = {}
                    sign_hits_dict[sample][target_name]['evalue'] = evalue
                    sign_hits_dict[sample][target_name]['score'] = score
                    sign_hits_dict[sample][target_name]['bias'] = bias
                    sign_hits_dict[sample][target_name]['dom_nr'] = dom_nr
                    sign_hits_dict[sample][target_name]['bestdom_evalue'] = bestdom_evalue
                    sign_hits_dict[sample][target_name]['bestdom_score'] = bestdom_score
                    sign_hits_dict[sample][target_name]['bestdom_bias'] = bestdom_bias
                    #sign_hits_dict[sample][target_name]['gc_content'] = gc_content
                    #sign_hits_dict[sample][target_name]['sequence'] = sequence


                    # print(sample+"\t"+target_name+"\t"+evalue+"\t"+score+"\t"+bias+"\t"+dom_nr+"\t"+bestdom_evalue+"\t"+bestdom_score+"\t"+bestdom_bias)

def parse_metadata():
    kngdm = re.compile(".*k__([a-zA-Z)]*)")
    phylum = re.compile(".*p__([a-zA-Z)]*)")
    clas = re.compile(".*c__([a-zA-Z)]*)")
    order = re.compile(".*o__([a-zA-Z)]*)")
    fam = re.compile(".*f__([a-zA-Z)]*)")
    genus = re.compile(".*g__([a-zA-Z)]*)")
    species = re.compile(".*s__([a-zA-Z)]*)")

    # open bin to taxonomy mapping file
    with open(bin_to_tax,"r")as inp:
        for line in inp:
            if re.match(pattern, line):  # if line is entry
                l = line.split(";")
                #print(l)
                sample = l[0]
                #if not sign_hits_dict.__contains__(sample):  # are there significant hits for current sample?
                    #continue

                completeness = l[2]
                contamination = l[3]
                perc5s = l[4]
                perc16s = l[5]
                perc23s = l[6]
                trnas = l[7]
                hr = l[8]
                refseq = l[9]
                lineage = l[10]
                lineage = lineage.split(";")

                if kngdm.match(line):
                    k = kngdm.search(line).group(1)
                else:
                    k = "NA"
                if phylum.match(line):
                    p = phylum.search(line).group(1)
                else:
                    p = "NA"
                if clas.match(line):
                    c = clas.search(line).group(1)
                else:
                    c = "NA"
                if order.match(line):
                    o = order.search(line).group(1)
                else:
                    o = "NA"
                if fam.match(line):
                    f = fam.search(line).group(1)
                else:
                    f = "NA"
                if genus.match(line):
                    g = genus.search(line).group(1)
                else:
                    g = "NA"
                if species.match(line):
                    s = species.search(line).group(1)
                else:
                    s = "NA"

                meta_dict[sample] = {}
                meta_dict[sample]['completeness'] = completeness
                meta_dict[sample]['contamination'] = contamination
                meta_dict[sample]['perc5s'] = perc5s
                meta_dict[sample]['perc16s'] = perc16s
                meta_dict[sample]['perc23s'] = perc23s
                meta_dict[sample]['trnas'] = trnas
                meta_dict[sample]['hr'] = hr
                meta_dict[sample]['refseq'] = refseq
                meta_dict[sample]['kingdom'] = k
                meta_dict[sample]['phylum'] = p
                meta_dict[sample]['class'] = c
                meta_dict[sample]['order'] = o
                meta_dict[sample]['family'] = f
                meta_dict[sample]['genus'] = g
                meta_dict[sample]['species'] = s



parse_hmmsearch_output()
#parse_metadata()
#print(sign_hits_dict)
#print(meta_dict)
print_dictionaries()
#print_fasta()