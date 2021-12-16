#!/usr/bin/env python3

import argparse
import glob
import json
import re
import os

parser = argparse.ArgumentParser(
    description="This script parses a bunch of hmmsearch output files for different samples"
                "of the same environment (e.g. marine) and summarizes it")

parser.add_argument("--input", help="path to input crisprfinder result folders (i.e. jgi ids (33000.._result))",
                    required=True)
parser.add_argument("--output", help="path to output folder", required=True)

args = parser.parse_args()
results_dir = args.input
output_dir = args.output

## open each result.json and collect info
## general info on CRISPRs and Cas for each sequence
## write sequences to fasta (files for spacers, DRs, Flanks)



def write_crispr_info(sequence_dict):
    global first_line
    if first_line:
        crispr_info.write("sample_id,seq_length,seq_st,crispr_name,evidence_level,nr_spacers,start,end,dr_length,dr_conservation,dr_id,spacers_conservation\n")
        first_line = False

    for crispr in sequence_dict['Crisprs']:  # each 'crispr' is a dictionary
        crispr_info.write(
            sample_id + "," + str(sequence_dict['Length']) + "," + str(sequence_dict['AT']) + "," + crispr['Name'] + "," +
            str(crispr['Evidence_Level']) + "," + str(crispr['Spacers']) + "," + str(crispr['Start']) + "," +
            str(crispr['End']) + "," + str(crispr['DR_Length']) + "," + str(crispr['Conservation_DRs']) + "," +
            crispr['Repeat_ID'] + "," + str(crispr['Conservation_Spacers']) + "\n")


def write_fasta(crisprs_list):
    for crispr_dict in crisprs_list:  # each 'crispr' is a dictionary
        ## write consensus repeats for each array to fasta
        #cons_repeats_fasta.write(">{}|{}\n".format(sample_id, crispr_dict['Name']))
        #cons_repeats_fasta.write(crispr_dict['DR_Consensus'] + "\n")

        for region_dict in crispr_dict['Regions']:
            if region_dict['Type'] == 'Spacer':
                spacers_fasta.write(">{}|{}\n".format(sample_id,crispr_dict['Name']))
                spacers_fasta.write(region_dict['Sequence']+"\n")
                #rsr_fasta.write(">{}_rsr_{}\n".format(sample_id, crispr_dict['Name']))
                #rsr_fasta.write(crispr_dict['DR_Consensus'] + region_dict['Sequence'] + crispr_dict['DR_Consensus'] + "\n")
                #rsr_fasta.write(">{}_rs_{}\n".format(sample_id, crispr_dict['Name']))
                #rsr_fasta.write(crispr_dict['DR_Consensus'] + region_dict['Sequence'] + "\n")
                #rsr_fasta.write(">{}_sr_{}\n".format(sample_id, crispr_dict['Name']))
                #rsr_fasta.write(region_dict['Sequence'] + crispr_dict['DR_Consensus'] +"\n")
                #rsr_fasta.write(">{}_s_{}\n".format(sample_id, crispr_dict['Name']))
                #rsr_fasta.write(region_dict['Sequence'] + "\n")
            # if region_dict['Type'] == 'DR':
                cons_repeats_fasta.write(">{}|{}\n".format(sample_id,crispr_dict['Name']))
                cons_repeats_fasta.write(region_dict['Sequence']+"\n")
            if region_dict['Type'] == 'LeftFLANK':
                if not region_dict['Sequence'] == "UNKNOWN":
                    lf_fasta.write(">{}|{}|{}\n".format(sample_id,crispr_dict['Name'],region_dict['Leader']))
                    lf_fasta.write(region_dict['Sequence']+"\n")
            if region_dict['Type'] == 'RightFLANK':
                if not region_dict['Sequence'] == "UNKNOWN":
                    rf_fasta.write(">{}|{}|{}\n".format(sample_id,crispr_dict['Name'],region_dict['Leader']))
                    rf_fasta.write(region_dict['Sequence']+"\n")



if __name__ == "__main__":

    #if os.path.getsize("{}/crisprs_info.csv".format(output_dir)) > 0:
        #os.system("rm {}/crisprs_info.csv".format(output_dir))

    ## create output files


    for result_folder in glob.glob("{}/*_result".format(results_dir)):

        #sample_id = re.match(re.compile(r".*/([0-9]*)_result$"), result_folder).group(1)
        sample_id = re.match(re.compile(r".*/(.*)_crisprcasfinder_result$"), result_folder).group(1)
        print(sample_id)

        crispr_info = open("{}/{}_crisprs_info.csv".format(output_dir,sample_id), "w")
        spacers_fasta = open("{}/{}_spacers.fasta".format(output_dir,sample_id), "w")
        cons_repeats_fasta = open("{}/{}_consensus_repeats.fasta".format(output_dir,sample_id), "w")
        lf_fasta = open("{}/{}_left_flanks.fasta".format(output_dir,sample_id), "w")
        rf_fasta = open("{}/{}_right_flanks.fasta".format(output_dir,sample_id), "w")
        #rsr_fasta = open("{}/{}_rsr.fasta".format(output_dir, sample_id), "w")
        first_line = True


        result_file = open("{}/result.json".format(result_folder), "r")
        result = json.load(result_file)

        for sequence in result['Sequences']:  # each 'sequence' is a dictionary

            if len(sequence['Crisprs']) > 0:  # crisprs present
                write_crispr_info(sequence)
                write_fasta(sequence['Crisprs'])


    result_file.close()
    #rsr_fasta.close()
    crispr_info.close()
    spacers_fasta.close()
    cons_repeats_fasta.close()
    lf_fasta.close()
    rf_fasta.close()
