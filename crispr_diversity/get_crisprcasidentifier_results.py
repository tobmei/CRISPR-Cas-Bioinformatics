#!/usr/bin/env python3

import argparse
import glob
import json
import re
import os

parser = argparse.ArgumentParser(
    description="This script parses the results of CRISPRCasIdentifier")

parser.add_argument("--input", help="path to input crisprcasidentifier result folders", required=True)
parser.add_argument("--output", help="path to output folder", required=False)
parser.add_argument("--hmm", help="which hmm model to use?", required=True)

args = parser.parse_args()
results_dir = args.input
output_dir = args.output
hmm_model = args.hmm

## results_dir has crisprcasidentifier_33000xxx files with cas cassette predictions
## HMM,cassette_id,classifier,regressor,predicted_label
## HMM1,1,ERT,ERT,"[('CAS-VI-B', 0.84), ('CAS-I-U', 0.06), ('CAS-I-F', 0.04), ('CAS-I-C', 0.02), ('CAS-I-D', 0.02), ('CAS-I-A', 0.01), ('CAS-III-A', 0.01)]"
## HMM1,2,ERT,ERT,"[('CAS-VI-B', 0.64), ('CAS-III-D', 0.23), ('CAS-II-C', 0.05), ('CAS-V-A', 0.03), ('CAS-II-A', 0.02), ('CAS-I-U', 0.01), ('CAS-III-A', 0.01), ('CAS-IV-A', 0.01)]"
## HMM1,3,ERT,ERT,"[('CAS-VI-B', 0.96), ('CAS-I-D', 0.02), ('CAS-I-A', 0.01), ('CAS-III-A', 0.01)]"

## build dictionary from result and give it to different write functions

## result_dict = {sample_id -> {HMM1 -> {cassette_id1 -> {first -> (CAS1,prob), second -> (CAS2,prob)}; casette_id2 -> {...}}; sample_id -> {...}; ...}

def write_type_distribution_per_sample(result_dict):
    ## sample| CASI-A| CASI-B|...
    ## 33001 |    2  |   4   |...

    # with open("{}subtype_dist_per_sample.csv", "w") as inp:
        print("sampleID,CAS-I-A,CAS-I-B,CAS-I-C,CAS-I-D,CAS-I-E,CAS-I-F,CAS-I-U,CAS-II-A,CAS-II-B,CAS-II-C,CAS-III-A,"
              "CAS-III-B,CAS-III-C,CAS-III-D,CAS-IV-A,CAS-V-A,CAS-VI-A,CAS-VI-B")
        for smpl_id, hmm_dict in result_dict.items():
            casIA=casIB=casIC=casID=casIE=casIF=casIU=casIIA=casIIB=casIIC=casIIIA=casIIIB=casIIIC=casIIID=casIVA=casVA=casVIA=casVIB = 0
            for hmm, cassette_dict in hmm_dict.items():
                if hmm == hmm_model:
                    for cassette_id, pred_dict in cassette_dict.items():
                        type = pred_dict['first'][0]
                        if type == "CAS-I-A": casIA += 1
                        if type == "CAS-I-B": casIB += 1
                        if type == "CAS-I-C": casIC += 1
                        if type == "CAS-I-D": casID += 1
                        if type == "CAS-I-E": casIE += 1
                        if type == "CAS-I-F": casIF += 1
                        if type == "CAS-I-U": casIU += 1
                        if type == "CAS-II-A": casIIA += 1
                        if type == "CAS-II-B": casIIB += 1
                        if type == "CAS-II-C": casIIC += 1
                        if type == "CAS-III-A": casIIIA += 1
                        if type == "CAS-III-B": casIIIB += 1
                        if type == "CAS-III-C": casIIIC += 1
                        if type == "CAS-III-D": casIIID += 1
                        if type == "CAS-IV-A": casIVA += 1
                        if type == "CAS-V-A": casVA += 1
                        if type == "CAS-VI-A": casVIA += 1
                        if type == "CAS-VI-B": casVIB += 1

            print(smpl_id+","+str(casIA)+","+str(casIB)+","+str(casIC)+","+str(casID)+","+str(casIE)+","+str(casIF)+","+str(casIU)+","+
                      str(casIIA)+","+str(casIIB)+","+str(casIIC)+","+str(casIIIA)+","+str(casIIIB)+","+str(casIIIC)+","+
                      str(casIIID)+","+str(casIVA)+","+str(casVA)+","+str(casVIA)+","+str(casVIB))

def write_prob_distribution(result_dict):
    ## sample| cassette_id| first pick | first prob | ..
    ## 33001 |  33001_1   |   CASIA    |    0.9
    ## 33001 |  33001_1   |   CASIB    |    0.6
    ## 33002 |  33002_3   |   CASIVA   |    0.7
    # with open("{}subtype_dist_per_sample.csv", "w") as inp:
    print("sampleID,cassette_id,first_pred,first_prob,second_pred,second_prob,prob_diff")
    for smpl_id, hmm_dict in result_dict.items():
        for hmm, cassette_dict in hmm_dict.items():
            if hmm_model == hmm:
                for cassette_id, pred_dict in cassette_dict.items():
                    unique_cassetteid = smpl_id+"_"+cassette_id  # create unique id for each cassette: 330001_3
                    first_type = pred_dict['first'][0]
                    first_prob = pred_dict['first'][1]
                    second_type = pred_dict['second'][0]
                    second_prob = pred_dict['second'][1]
                    third_type = pred_dict['third'][0]
                    third_prob = pred_dict['third'][1]
                    #prob_diff = "NA" if second_type == "NA" else float(first_prob) - float(second_prob)

                    print(smpl_id+","+unique_cassetteid+","+first_type+","+first_prob+","+second_type+","+second_prob+","+third_type+","+third_prob)


if __name__ == "__main__":

    result_dict = {}

    #for result_file in glob.glob("{}/crisprcasidentifier_*".format(results_dir)):
    #print(results_dir)
    for result_file in glob.glob("{}/*_predictions".format(results_dir)):
        #sample_id = re.match(re.compile(r".*/crisprcasidentifier_([0-9]*)$"), result_file).group(1)
        sample_id = re.match(re.compile(r".*\/(.*)_1000_contigs.fa_predictions"), result_file).group(1)
        #print(sample_id)

        with open(result_file, "r") as inp:
            for line in inp:
                line_strip = line.strip().split(",")
                if line_strip[0] == "HMM": ## header line
                    continue

                hmm = line_strip[0]
                cassette_id = line_strip[1]

                if not result_dict.__contains__(sample_id):
                    result_dict[sample_id] = {}

                if not result_dict[sample_id].__contains__(hmm):
                    result_dict[sample_id][hmm] = {}

                result_dict[sample_id][hmm][cassette_id] = {}
                cas_pred = re.findall(re.compile(r"(CAS-[IV]*-[ABCDEFU])', ([01]\.[0-9]+)"), line)

                first_pick_type = cas_pred[0][0]
                first_pick_prob = cas_pred[0][1]
                scnd_pick_type = "NA" if len(cas_pred) == 1 else cas_pred[1][0]
                scnd_pick_prob = "NA" if len(cas_pred) == 1 else cas_pred[1][1]
                third_pick_type = cas_pred[2][0] if len(cas_pred) > 2 else "NA"
                third_pick_prob = cas_pred[2][1] if len(cas_pred) > 2 else "NA"
                result_dict[sample_id][hmm][cassette_id] = {}
                result_dict[sample_id][hmm][cassette_id]['first'] = (first_pick_type, first_pick_prob)
                result_dict[sample_id][hmm][cassette_id]['second'] = (scnd_pick_type, scnd_pick_prob)
                result_dict[sample_id][hmm][cassette_id]['third'] = (third_pick_type, third_pick_prob)

            #     break
            # break

    write_type_distribution_per_sample(result_dict)
    #write_prob_distribution(result_dict)