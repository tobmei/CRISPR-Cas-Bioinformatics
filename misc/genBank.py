from Bio import Entrez
import re
import csv

count = 0
result = {}

# genbank_pattern = re.compile("^(.*\.\d)")

with open("/Volumes/IBVT/spacerome/inline-supplementary-material-6.txt") as f:
    for line in f:
        if count == 0:  # skip first line --> header
            count += 1
            continue
        count += 1
        line = line.split()
        spacerID = line[0]
        target = line[1]  # Phage? could also be prophage. check target tax
        targetAcc = line[2]  # protospacer containing phage genome
        # print(spacerID)
        genbankAcc = re.search(re.compile("^([A-Z]*[0-9]*\.?\d?)"), spacerID).group(1)

        Entrez.email = "tobias.meier@ibvt.uni-stuttgart.de"  # Always tell NCBI who you are
        handle = Entrez.esummary(db="nucleotide", id=genbankAcc)
        record = Entrez.read(handle)
        title = record[0]['Title']
        #print(record)

        if re.match("Staphylococcus|Streptococcus", title):  # i am only interested in those, since they share some spacers

            if not result.__contains__(targetAcc):
                result[targetAcc] = []

            organism = "Staphylo" if re.match("Staphylococcus", title) else "Strepto"
            result[targetAcc].append(organism + "_" + spacerID)

            if result[targetAcc].__len__() > 1:
                print("##########shared spacer##########")
                print(targetAcc)
                print(result[targetAcc])

            print(organism + "_" + spacerID)

w = csv.writer(open("output.csv", "w"))
for key, val in result.items():
    w.writerow([key, val])


