import argparse
import collections, sys
from Bio import Seq, SeqIO, SeqRecord
import re
import logging
import multiprocessing
import pickle


#debruijn implementation based on 
#https://pmelsted.wordpress.com/2013/11/23/naive-python-implementation-of-a-de-bruijn-graph/

def twin(km):
    return Seq.reverse_complement(km)


def get_kmers(seq, k):
    for i in range(len(seq) - k + 1):
        yield seq[i:i + k]


def fw(km):
    for x in 'ACGT':
        yield km[1:] + x


def bw(km):
    for x in 'ACGT':
        yield x + km[:-1]


def process_chunk(batch, batch_nr):
    logging.info("processing batch nr: {} -- {} reads".format(batch_nr, len(batch)))

    kmers = collections.Counter()
    for read in batch:
        read = read.seq
        seq_s = str(read)
        seq_l = seq_s.split('N')  # handle Ns
        for seq in seq_l:
            for km in get_kmers(seq, k):
                kmers.update({km: 1})
            seq = twin(seq)
            for km in get_kmers(seq, k):
                kmers.update({km: 1})

    logging.info("finished batch nr: {}".format(batch_nr))
    return kmers


def mycallback(kmers):
    #logging.info("merging kmers...")
    global kmers_dict
    kmers_dict += kmers
    #logging.info("done merging")


def build(fn, k=31, limit=1):
    batch_size = 1000
    workers = 4

    for f in fn:
        #reads = SeqIO.parse(f, 'fastq')
        record_iter = SeqIO.parse(open(f), "fastq")

        # create a pool of workers
        logging.info("creating multiprocessing pool with {} workers...".format(workers))
        logging.info("batch size: {}".format(batch_size))
        pool = multiprocessing.Pool(processes=workers)
        for i, batch in enumerate(batch_iterator(record_iter, batch_size)):
            p = pool.apply_async(process_chunk, args=(batch,i,), callback=mycallback)
        pool.close()
        pool.join()


    global kmers_dict
    logging.info("removing unique k-mers...")
    # TODO: add mercy kmers
    d1 = [x for x in kmers_dict if kmers_dict[x] <= limit]  # remove unique k-mers
    for x in d1:
        del kmers_dict[x]

    logging.info("done")
    return kmers_dict


def contig_to_string(c):
    return c[0] + ''.join(x[-1] for x in c[1:])


def get_contig(kmers, km):
    c_fw = get_contig_forward(kmers, km)

    c_bw = get_contig_forward(kmers, twin(km))

    if km in fw(c_fw[-1]):
        c = c_fw # if circular
    else:
        c = [twin(x) for x in c_bw[-1:0:-1]] + c_fw #concat reverse complement of - strand to + strand
    return contig_to_string(c), c


def get_contig_forward(kmers, km):
    c_fw = [km]

    while True:
        if sum(x in kmers for x in fw(c_fw[-1])) != 1: # is there any, but only one k-mer in kmers that extends current k-mer?
            break

        cand = [x for x in fw(c_fw[-1]) if x in kmers][0] # all k-mers that extend current k-mers. pick first (the only one)
        if cand == km or cand == twin(km):
            break  # break out of cycles or mobius contigs
        if cand == twin(c_fw[-1]):
            break  # break out of hairpins

        if sum(x in kmers for x in bw(cand)) != 1: # check if cand has single backwards kmer. if not, there is a branch
            break

        c_fw.append(cand)

    return c_fw


def all_contigs(kmers, k):
    done = set()
    r = []
    for x in kmers: #d = {kmer: multiplicity}  -> (multiplicity never used)
        if x not in done:
            s, c = get_contig(kmers, x)
            for y in c: # cross each kmer in contig off the list
                done.add(y)
                done.add(twin(y))
            r.append(s) # add string of contig

    G = {}
    heads = {}
    tails = {}
    for i, x in enumerate(r): # mark first and rev last kmers as + and -
        G[i] = ([], [])
        heads[x[:k]] = (i, '+')
        tails[twin(x[-k:])] = (i, '-')

    for i in G:
        x = r[i] # x = contig string
        for y in fw(x[-k:]):
            if y in heads:
                G[i][0].append(heads[y])
            if y in tails:
                G[i][0].append(tails[y])
        for z in fw(twin(x[:k])):
            if z in heads:
                G[i][1].append(heads[z])
            if z in tails:
                G[i][1].append(tails[z])

    return G, r


def print_GFA(G, cs, k):
    #spacer = ['TCCCATGGGAGCAGTGGTGGCACTCAAGA', 'AGTGCCATCTATTCCGTGAATGCAAAGA', 'TCGGGCGTGCCGATCCTGGCGGGGATCTA','GAGCACTACCACGTCAGCACCCGTCAGCC']
    spacer = []

    gfa_output = open("output/k{}.gfa".format(k), "w")

    gfa_output.write("H\tVN:Z:1.0\n")
    for i, x in enumerate(cs):
        gfa_output.write("S\t%d\t%s\n" % (i, x))

        # find spacer in contigs
        if sum(y in x for y in spacer) > 0:
            logging.info("found spacer {} in node {}".format(x,i))

    for i in G:
        for j, o in G[i][0]:
            gfa_output.write("L\t%d\t+\t%d\t%s\t%dM\n" % (i, j, o, k - 1))
        for j, o in G[i][1]:
            gfa_output.write("L\t%d\t-\t%d\t%s\t%dM\n" % (i, j, o, k - 1))

    logging.info("gfa output written to {}".format(gfa_output.name))
    gfa_output.close()


def batch_iterator(iterator, batch_size):
    """Returns lists of length batch_size.

    This can be used on any iterator, for example to batch up
    SeqRecord objects from Bio.SeqIO.parse(...), or to batch
    Alignment objects from Bio.AlignIO.parse(...), or simply
    lines from a file handle.

    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    """
    entry = True  # Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = iterator.__next__()
            except StopIteration:
                entry = None
            if entry is None:
                # End of file
                break
            batch.append(entry)
        if batch:
            yield batch



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script build a de Bruijn graph")
    parser.add_argument("--k", type=int)
    parser.add_argument("--reads", nargs='+')
    parser.add_argument("--pickle", help="path to file with pickled kmers")
    args = parser.parse_args()

    ## set up logging
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    screen_handler = logging.StreamHandler(stream=sys.stderr)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(screen_handler)

    kmers_dict = collections.Counter()

    k = args.k

    if args.pickle:
        logging.info("loading pickled kmers..")
        kmers_dict = pickle.load(open(args.pickle, 'rb'))
    else:
        logging.info("building deBruijn graph for {} with k = {}".format(args.reads, k))
        build(args.reads, k, 1)
        # pickle kmers_dict
        #logging.info("pickling kmers...")
        #outfile = open("../output/pickled_kmers_dict_{}".format(k), 'wb')
        #pickle.dump(kmers_dict, outfile)
        #outfile.close()
        logging.info("done")

    logging.info("merging linear paths...")
    G, cs = all_contigs(kmers_dict, k)
    logging.info("done")

    print_GFA(G, cs, k)
    logging.info("all done!")





