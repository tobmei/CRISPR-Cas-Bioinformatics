import sys

#read mapping file into dictionary
mapping = dict()
with open(sys.argv[1], "r") as f:
    for line in f:
        line = line.strip("\n").split(",")
        mapping[line[0]] = line[1]
        #print(line)


c = 0
for line in sys.stdin:
    if line.startswith(">"):
        acc = line.split("|")[2].split(".")[0]
        if acc not in mapping.keys():
            c = c+1
            sys.stderr.write("no tax id found for "+acc+"\n")
            continue
        taxid = mapping[acc]
        #print(line.strip("\n"))
        #print(acc)
        #print(taxid)
        line = line.strip("\n").split("|")
        line[0] = ">kraken:taxid|"+taxid+"|acc|"
        print('|'.join(line))
        continue
    print(line.strip("\n"))

sys.stderr.write(str(c)+" missing mappings\n")
