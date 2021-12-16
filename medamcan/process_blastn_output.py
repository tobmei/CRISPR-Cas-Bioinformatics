#!/usr/bin/env python3

import sys
import glob
import os
import re

opt_dir = sys.argv[1]
ncbi_dir = sys.argv[2]
gen_dir = sys.argv[3]

sig_ids=['k145_97894','k145_41331','k145_29615','k145_87735','k145_12706','k145_65175','k145_105896','k145_27305','k145_31694','k145_79339','k145_21558','k145_103030','k145_39871','k145_108726','k145_51546','k145_106020','k145_28219','k145_108009','k145_50826','k145_36755','k145_83484','k145_83998','k145_85566','k145_1815','k145_93991','k145_96532','k145_22143','k145_109181','k145_99977','k145_100954','k145_8923','k145_20736','k145_40340','k145_79832','k145_59284','k145_91457','k145_114462','k145_77','k145_27313','k145_58114','k145_60056','k145_57400','k145_34612','k145_80587','k145_37911','k145_50845','k145_106253','k145_79309','k145_46847','k145_47715','k145_57395','k145_112905','k145_73424','k145_90079','k145_90579','k145_16037','k145_30446','k145_42545','k145_33849','k145_101666','k145_9487','k145_68573','k145_86358','k145_40268','k145_36766','k145_86931','k145_107135','k145_62104','k145_27077','k145_114437','k145_114444','k145_44043','k145_75672','k145_58739','k145_28527','k145_81215','k145_3632','k145_11543','k145_50838','k145_215','k145_45260','k145_114167','k145_105854','k145_34586','k145_65995','k145_86670','k145_25097','k145_28529','k145_10682','k145_27310','k145_108870','k145_8398','k145_62803','k145_108985','k145_72373','k145_59191','k145_74334','k145_17761','k145_99660','k145_26667','k145_15498','k145_84515','k145_67669','k145_39384','k145_110079','k145_34615','k145_72519','k145_34938','k145_77448','k145_4597','k145_84727','k145_43637','k145_77075','k145_108842','k145_97348','k145_80753','k145_73249','k145_81487','k145_29668','k145_73251','k145_47674','k145_40286','k145_71878','k145_4940','k145_113937','k145_19518','k145_96589','k145_38170','k145_26663','k145_89205','k145_19591','k145_61278','k145_68686','k145_110184','k145_58086','k145_20485','k145_47808','k145_49228','k145_25922','k145_94940','k145_86495','k145_36800','k145_61685','k145_12595','k145_30069','k145_112117','k145_99203','k145_86366','k145_86666']

for opt_out in glob.glob(opt_dir+"/*"):
    # if os.stat(opt_out).st_size == 0: #file is empty
    #     continue

    #print(os.path.basename(opt_out))
    ncbi = re.match("^(.*)_blastn.*", os.path.basename(opt_out)).group(1)
    # print(ncbi)
    if ncbi != "SRP257201":
        continue

    #check if ncbi blast hits to viruses exist exist
    # if os.stat("{}/{}_blastn_results_nt".format(ncbi_dir/ncbi)).st_size == 0:
    #     continue

    with open("{}_blastn_compare_ncbi_opt".format(ncbi), "w") as outfile:

        with open("{}/{}_blastn_results.out".format(opt_dir, ncbi), "r") as opt_file:
            for line in opt_file:
                line = line.split("\t")
                bitscore = line[10]
                target = line[1]

                if target in sig_ids:
                    outfile.write("MG_vir\t{}\t{}\n".format(target,bitscore))
                else:
                    outfile.write("MG\t{}\t{}\n".format(target,bitscore))

        with open("{}/{}_blastn_results_gen.out".format(gen_dir, ncbi), "r") as gen_file:
            for line in gen_file:
                line = line.split("\t")
                bitscore = line[10]
                target = line[1]

                if target in sig_ids:
                    outfile.write("MG_default_vir\t{}\t{}\n".format(target,bitscore))
                else:
                    outfile.write("MG_default\t{}\t{}\n".format(target,bitscore))

        with open("{}/{}_blastn_results_nt.out".format(ncbi_dir,ncbi), "r") as nt_file:
            for line in nt_file:
                line = line.split("\t")
                bitscore = line[10]
                target = line[1]

                outfile.write("NCBI_nt\t{}\t{}\n".format(target,bitscore))

        with open("{}/{}_blastn_results_viruses.out".format(ncbi_dir,ncbi), "r") as vir_file:
            for line in vir_file:
                line = line.split("\t")
                bitscore = line[10]
                target = line[1]

                outfile.write("NCBI_vir\t{}\t{}\n".format(target,bitscore))



