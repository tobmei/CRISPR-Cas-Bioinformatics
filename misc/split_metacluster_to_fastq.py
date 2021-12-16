from Bio import SeqIO
import sys
import re

metacluster_out = sys.argv[1]
reads_r1 = sys.argv[2]
reads_r2 = sys.argv[3]

print("indexing reads_r1")
record_r1 = SeqIO.index(reads_r1, "fastq")
print("indexing reads_r2")
record_r2 = SeqIO.index(reads_r2, "fastq")
print("done")

current_cluster = '0'
r1_arr = []
r2_arr = []

with open(metacluster_out, "r") as handle:
    for line in handle:

        if line.startswith(">"):
            # its a fasta header
            rec_id = line.split()[0].strip(">")
            if re.match(".*1:N:0.*", line) is not None:
                r1 = record_r1.get(rec_id)
                r1_arr.append(r1.format("fastq"))
            else:
                r2 = record_r2.get(rec_id)
                r2_arr.append(r2.format("fastq"))

        else:
            current_cluster = line.split()[2]
            print("Current Cluster: {}".format(current_cluster))

            if current_cluster > '0': #write reads for previous cluster to file
                print("write fastqs...")
                file = open("{}_R1.fastq".format(current_cluster), "w")
                for read in r1_arr:
                    file.write(read)
                file.close()
                file = open("{}_R2.fastq".format(current_cluster), "w")
                for read in r2_arr:
                    file.write(read)
                file.close()
                r1_arr = []
                r2_arr = []






