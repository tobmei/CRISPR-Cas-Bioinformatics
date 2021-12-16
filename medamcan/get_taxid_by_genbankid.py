import argparse
import multiprocessing
import sys
import os
import subprocess
import lxml.etree
from Bio import Entrez
import re
import sys
from itertools import islice
import numpy
import json


def process_chunk(chunk, count):
    if len(chunk) == 0:
        return []
    sys.stderr.write("processing chunk " + str(count) + " of size " + str(len(chunk)) + " ...\n")
    id = 0
    taxid = 0
    res = []
    ids = [''.join(x.splitlines()) for x in chunk]
    s = ','.join(ids)
    #mv out handle = Entrez.esummary(db='nucleotide', id=s, rettype="gb", retmode="json")
    handle = Entrez.esummary(db='taxonomy', id=855, rettype="gb", retmode="json")
    text = handle.read()
    js = json.loads(text)
    #entry = lxml.etree.parse(handle)
    #primary_acc = entry.xpath('//eSummaryResult/DocSum/@TaxId')[0]
    #hits = re.findall("\"taxid\":([0-9]+)", text)
    if 'result' not in js.keys():
        return res
    for k,v in js['result'].items():
        if k=="uids":
            continue
        res.append(v['caption'] + "," + str(v['taxid']))

    handle.close()
    return res


def multi(lines):
    size = 500
    start = 0
    stop = size
    chunks_nr = int(len(lines) / size) + 1
    for i in range(0, chunks_nr + 1):
        res = process_chunk(list(islice(iter(lines), start, stop)), i)
        if len(res) > 0:
            outlist.append(res)
        start = stop + 1
        stop = stop + size + 1

    if stop > len(lines):
        return

    return


Entrez.email = 'tobias.meier@ibvt.uni-stuttgart.de'

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()  # readlines creates a list of the lines

outlist = []
multi(lines)

with open(("out.txt"), "w") as f:
    for cs in outlist:
        for c in cs:
            f.write(c+"\n")
