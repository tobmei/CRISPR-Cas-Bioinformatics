#!/usr/bin/env python3

import argparse
import glob
import re
import subprocess
parser = argparse.ArgumentParser(description="This script collects meta data for jgi metagenomes")

parser.add_argument("--jgi_input", help="path to input folders (i.e. jgi ids (33000..))", required=True)
parser.add_argument("--output", help="path to output file", required=True)

args = parser.parse_args()
jgi_in_dir = args.jgi_input
output_dir = args.output

print("mg_id,analysis_project_id,jgi_project_id,jgi_species_code,combined_sample,domain,genome_size,genome_type,ir_class,is_public,phylum,seq_cov_file")

# patterns to search for in .config file
# some patterns might not be present
patterns = ["analysis_project_id","jgi_project_id","jgi_species_code","combined_sample_flag","domain","genome_size",
            "genome_type","ir_class","ir_order","is_public","phylum","seq_coverage_file","submission_date"]


# jgi folders are .tar.gz
# only extract *.config file, get contents, then delete
for jgi_archive in glob.glob("{}/33*.tar.gz".format(jgi_in_dir)):
    print(jgi_archive)
    sample_id = re.match(re.compile(r".*/([0-9]*)\.tar\.gz$"), jgi_archive).group(1)
    print(sample_id)
    subprocess.call(["tar", "-C", output_dir, "-xzf", jgi_archive, "{}/{}.config".format(sample_id,sample_id)])

    break
    # for file in glob.glob("{}/*.config".format(jgi_archive)):
    #     f = open(file,"r")
    #     content = f.read()
    #     content = content.replace("\n",";;")
    #     for pattern in patterns:
    #         match = re.match(re.compile(r".*\.{} (.*?);;.*".format(pattern)), content)
    #         if not match is None:
    #             result = match.group(1)
    #         else:
    #             result = "NA"
    #
    #         if pattern == patterns[-1]:
    #             print(result)
    #         else:
    #             print(result+","),
    #
    #     f.close()


