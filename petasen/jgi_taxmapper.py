#!/usr/bin/env python3

import argparse
import re
import glob
from Bio import SeqIO
from Bio import SearchIO
import subprocess

parser = argparse.ArgumentParser(
    description="This script parses a bunch of hmmsearch output files for different samples"
                "of the same environment (e.g. marine) and summarizes it")

parser.add_argument("--hmm_input", help="path to input files (i.e. hmmsearch output)", required=True)
parser.add_argument("--jgi_input", help="path to input folders (i.e. jgi ids (33000..))", required=True)
parser.add_argument("--evalue", default="10e-3", type=float, help="significance threshold", required=False)
parser.add_argument("--fasta", help="path to protein files", required=False)
parser.add_argument("--fasta_out", help="file to write fasta", required=False)

args = parser.parse_args()
evalue_thr = args.evalue
hmm_in_dir = args.hmm_input
jgi_in_dir = args.jgi_input
fasta = args.fasta
fasta_file = args.fasta_out

# input: path to 33000.. folders
# inpit: path to hmmsearch out files (33000.._domtblout)

config_file = "{}/*.config".format(jgi_in_dir)
jgi_id_pattern = ".*([0-9]{10})_.*$"

# write protein sequences to corresponding sig hits
# for every id in hit_ids, get corresponding fasta entry in
def print_protein_fasta(hit_ids):

    with open(fasta_file, "a") as inp:
        for jgi_id,hits in hit_ids.items():
            # create index of fasta file
            index = SeqIO.index("{}{}_proteins.faa".format(fasta,jgi_id), "fasta")
            for hit in hits:
                sequence = str(index.get(hit).seq)
                inp.write(">{}|{}\n".format(jgi_id,hit))
                inp.write(sequence+"\n")



def get_lineage(file, gene_id):
    homolog_gene_id=homolog_taxon_id=percent_identity=kingdom=phylum=clas=order=family=genus=species = " "

    grep = subprocess.Popen(["grep",gene_id,file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = grep.communicate()
    if grep.returncode == 1:  # i.e. no match found
        homolog_gene_id=homolog_taxon_id=percent_identity=kingdom=phylum=clas=order=family=genus=species = "NA"
    else:
        output = output.decode("utf-8").split()  # decode byte to string
        homolog_gene_id = output[1]
        homolog_taxon_id = output[2]
        percent_identity = output[3]
        lineage = output[4].split(";")
        if len(lineage)>0: kingdom = lineage[0]
        if len(lineage)>1: phylum = lineage[1]
        if len(lineage)>2: clas = lineage[2]
        if len(lineage)>3: order = lineage[3]
        if len(lineage)>4: family = lineage[4]
        if len(lineage)>5: genus = lineage[5]
        if len(lineage)>6: species = lineage[6]

    return homolog_gene_id, homolog_taxon_id, percent_identity, kingdom,phylum,clas,order,family,genus,species


def get_phylo_gene_id(gene_id):
    # get rid of last underscore: Ga0186617_107904_1 --> Ga0186617_1079041
    tmp = gene_id.split("_")
    return "{}_{}{}".format(tmp[0],tmp[1],tmp[2])


def parse_hmmsearch_output(file, phylo_dist_file, jgi_id):
    # read in hmmsearch output
    qresult = SearchIO.read(file, "hmmsearch3-domtab")

    for hit in qresult.hits:
        # for each significant hit
        if hit.evalue <= evalue_thr:  # if hit is below threshold
            hit_target_phylo_format = get_phylo_gene_id(hit.id)

            # get tax info for hit from jgi phylodist file
            homolog_gene_id,homolog_taxon_id,percent_identity, \
            kingdom,phylum,clas,order,family,genus,species = get_lineage(phylo_dist_file,hit_target_phylo_format)

            if not hit_ids.__contains__(jgi_id):
                hit_ids[jgi_id] = []
            hit_ids[jgi_id].append(hit.id)

            print(jgi_id+"\t"+hit.query_id+"\t"+hit.id+"\t"+str(hit.evalue)+"\t"+str(hit.bitscore)+"\t"+str(len(hit.hsps))+
                  "\t"+kingdom+"\t"+phylum+"\t"+clas+"\t"+order+"\t"+family+"\t"+genus+"\t"+species)

            #for hsp in hit.hsps:
            #print(jgi_id, hit.id, hit.query_id, hsp.domain_index,kingdom,phylum,clas,order,family,genus,species)



if __name__ == "__main__":

    # dictionary to store significant hits for each jgi_id
    # give it to print_fasta to create protein fasta file
    hit_ids = {}

    print("smaple_id\tquery\ttarget\tevalue\tbitscore\t#domain_hits\tkingdom\tphylum\tclass\torder\tfamily\tgenus\tspecies")
    for hmmsearch_out_file in glob.glob("{}/*domtblout".format(hmm_in_dir)):
        jgi_id = re.compile(jgi_id_pattern).search(hmmsearch_out_file).group(1)
        phylo_dist_file = "{}{}/{}.a.phylodist.txt".format(jgi_in_dir,jgi_id,jgi_id)
        #print("hmmsearch out file: {}".format(hmmsearch_out_file))
        #print("phylodist file: {}".format(phylo_dist_file))
        parse_hmmsearch_output(hmmsearch_out_file, phylo_dist_file, jgi_id)

    #print(hit_ids)
    if not fasta==None: print_protein_fasta(hit_ids)
