#!/usr/bin/env python

"""
Get run accession numbers and SRA download urls for given SRA sample name.
Adapted from https://gist.github.com/martijnvermaat/4619109
"""

import argparse
import sys
import os
import subprocess
import lxml.etree
from Bio import Entrez
import re
import json

Entrez.email = 'tobias.meier@ibvt.uni-stuttgart.de'


def error(message):
    sys.stderr.write(message + '\n')
    sys.exit(1)


def get_summary(id):
    #i = 1000
    handle = Entrez.esearch(db='sra', term=id, retmode="text")
    record = Entrez.read(handle)
    if len(record['IdList']) == 0:
        return 0
    id = record['IdList'][0]

    handle = Entrez.efetch(db='sra', id=id, retmode="text")
    entry = lxml.etree.parse(handle)
    source = entry.xpath('//SAMPLE/SAMPLE_NAME/SCIENTIFIC_NAME/text()')[0]
    #title = entry.xpath('//SAMPLE/TITLE/text()')[0]
    bases = entry.xpath('//Pool/Member/@bases')
    if len(bases) == 0:
        bases ="NA"
    #strategy = entry.xpath('//EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_STRATEGY/text()')
    s = str(source)

    return s

def get_ids(id):
    i = 1000
    handle = Entrez.esearch(db='nucleotide', term=id, retstart=i, retmax=10)
    record = Entrez.read(handle)
    results = record['IdList']
    return results

def get_taxid(id):
    i = 1000
    handle = Entrez.efetch(db='nucleotide', id=id, rettype="gb", retmode="text")
    text = handle.read()
    hit = re.search("taxon:([0-9]+)", text)
    taxid = hit.group(1)

    return taxid


def get_identifier(_id):
    handle = Entrez.efetch(db='sra', id=_id, retmode="text")
    read = handle.read()
    entry = lxml.etree.parse(handle)
    primary_acc = entry.xpath('//EXPERIMENT_PACKAGE_SET/EXPERIMENT_PACKAGE/STUDY/@accession')[0]
    run_acc = entry.xpath('//EXPERIMENT_PACKAGE_SET/EXPERIMENT_PACKAGE/RUN_SET/RUN/@accession')[0]
    return primary_acc, run_acc


def get_url(run):
    # ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/ERR/ERR006/ERR006600/ERR006600.sra
    url_template = 'ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/{leading3}/{leading6}/{all}/{all}.sra'
    return url_template.format(leading3=run[:3], leading6=run[:6], all=run)


def download(path, runid):
    prefetch = subprocess.Popen(['prefetch.2.10.5', '-p', '-O', path, runid])
    stdout, stderr = prefetch.communicate()
    if prefetch.returncode > 0:
        print(stderr)
    # sra file is in path/runid/runid.sra

    sra_file = "{}/{}/{}.sra".format(path,runid,runid)
    dump = subprocess.Popen(['fasterq-dump.2.10.5','-p', '-O', path, sra_file])
    stdout, stderr = dump.communicate()
    if dump.returncode > 0:
        print(stderr)

    # remove sra file
    print("removing {}/{}".format(path,runid))
    rm = subprocess.Popen(['rm', '-r', "{}/{}".format(path,runid)])
    stdout, stderr = rm.communicate()
    if rm.returncode > 0:
        print(stderr)


def main(id):
    _ids = get_taxid(id)
    accessions = {}
    file = open("../scripts/SraAccList.txt", "a")
    for _id in _ids:
        primary, runid = get_identifier(_id)
        if primary == 'ERP117839':
            print("skipping ERP117839")
            continue

        # does primaryID folder exist in cwd?
        path = "{}/{}".format(os.getcwd(), primary)
        if not os.path.exists(path):
            os.mkdir(path)

        download(path, runid)

        file.write(primary+","+runid+"\n")
        # if primary not in accessions:
        #     accessions[primary] = [run]
        # else:
        #     accessions[primary].append(run)
    # print("\t".join([args.sample, ";".join(accessions)]))
    # for k, v in accessions.items():
    #     print(k+"\t"+",".join(v))
    # print(accessions)
    file.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('-i', metavar='SAMPLE',
                        help='input (or any search term)')
    args = parser.parse_args()



    #sample ="((((public[Access]) AND metagenomic[Source]) AND wgs[Strategy]) AND paired[Layout]) AND illumina[Platform]"
#main(args.i)
total_bases = 0
with open("/home/tob/toStick/uni/common_ids.txt") as f:
    lines = f.readlines()
    for l in lines:
        l=l.rstrip()
        s = get_summary(l)
        print(l+","+str(s))
        #print(strat)
#get_summary("ERP113060")
print(total_bases)

