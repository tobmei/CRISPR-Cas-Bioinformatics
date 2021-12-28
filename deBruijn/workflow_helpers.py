from helpers.dbg_old import *
# g1 = gfapy.Gfa()
# g1.append("H\tVN:Z:1.0")
from helpers.dbg_old import *
# returns set of k-mers for given sequecne
def generate_kmers(sequence, k):
    # convert read to string
    read = str(sequence)

    # split the record into chunks of k-mers
    # and save it to array of k_mers
    k_mers = [read[i:i + k] for i in range(len(read) - k)]

    return k_mers

#function collects all the kmers together
#output is an argument passed by value where the function modifies output
def collect_kmers(kmers,output):
    for i in kmers:
        output.append(i)


# creates output in GFA format for given de Bruijn graph
def create_gfa_output(k_mers,gfa):
    graph = DeBruijnGraph(k_mers,len(k_mers[0]),gfa)
    graph.to_dot()
    return graph