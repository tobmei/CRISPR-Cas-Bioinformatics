#!/usr/bin/python

import os
import glob
import re
from collections import defaultdict
import sys
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# tips = sns.load_dataset("tips")
# print(tips)


cwd = os.getcwd() #dir with workflow output (job_1, job_2, ...)
ale_pattern = re.compile(".*ALEoutput.*")
covstat_pattern = re.compile('.*covstats.*')
log_pattern = re.compile(".*megahit\.log.*")
print(cwd)
results = defaultdict(lambda : defaultdict(dict)) #3d dictionary {a: {b: {k:v,k:v,k:v,...} } }
covstats = {}

for job_output in os.listdir(cwd):
    print(job_output)
    if os.path.isfile("/home/tmeier/medamcan/ref_assemblies/jobs/{}.yml".format(job_output)):
        job_file = open("/home/tmeier/medamcan/ref_assemblies/jobs/{}.yml".format(job_output),'r')
        contents = job_file.read()
        kmin = re.compile("megaKmin: (\d*)").search(contents).group(1)
        kmax = re.compile("megaKmax: (\d*)").search(contents).group(1)
        kstep = re.compile("megaKstep: (\d*)").search(contents).group(1)
        prunelevel = re.compile("megaPruneLevel: (\d*)").search(contents).group(1)
        nomercy = re.compile("megaNoMercy: (.*)").search(contents).group(1)
        nobubble = re.compile("megaNoBubble: (.*)").search(contents).group(1)

    for subdr, dirs, files in os.walk(job_output): #files = list of file names
        for file in files: #all workflow output files

            #read ale output
            if ale_pattern.match(file):
                sample = re.compile("^(.*)\.fastq\.gz.*").search(file).group(1)

                with open(cwd+"/"+job_output+"/"+file) as f:
                    for line in f:
                        if line.startswith('#'):
                            match = re.compile("# ALE_score: (.*)").search(line)
                            if not match == None:
                                results[job_output][sample]['ALE_score'] = match.group(1)
                                continue
                            match = re.compile("# numContigs: (.*)").search(line)
                            if not match == None:
                                results[job_output][sample]['numContigs'] = match.group(1)
                                continue
                            match = re.compile("# totalAssemLen: (.*)").search(line)
                            if not match == None:
                                results[job_output][sample]['totalAssemLen'] = match.group(1)
                                continue
                            match = re.compile("# totalReads: (.*)").search(line)
                            if not match == None:
                                results[job_output][sample]['totalReads'] = match.group(1)
                                continue
                            match = re.compile("# totalMappedReads: (.*)").search(line)
                            if not match == None:
                                results[job_output][sample]['totalMappedReads'] = match.group(1)
                                results[job_output][sample]['mappedFraction'] = float(results[job_output][sample]['totalMappedReads'])/float(results[job_output][sample]['totalReads'])
                                continue

                        else:
                            break

                results[job_output][sample]['kmin'] = kmin
                results[job_output][sample]['kmax'] = kmax
                results[job_output][sample]['kstep'] = kstep
                results[job_output][sample]['prunelevel'] = prunelevel
                results[job_output][sample]['nomercy'] = nomercy
                results[job_output][sample]['nobubble'] = nobubble

            #read megahit log
            if log_pattern.match(file):
                sample = re.compile("^(.*)\.fastq\.gz.*").search(file).group(1)
                #read log file
                for line in reversed(open(cwd+"/"+job_output+"/"+file).readlines()):
                    match = re.compile("^--.*max\s(\d*)\sbp.*N50\s(\d*).*").search(line)
                    if not match == None:
                        results[job_output][sample]['max_contig'] = match.group(1)
                        results[job_output][sample]['n50'] = match.group(2)
                        break






            #read mapping coverage stats
            # if covstat_pattern.match(file):
            #     sample = re.compile("^(.*)\.fastq\.gz.*").search(file).group(1)
            #     #read covstat file
            #     cmd = ' cat {}/{}/{} | cut -f 10'.format(cwd,job_output,file)
            #     result = subprocess.check_output(cmd, shell=True)
            #     result = result.strip('Median_fold')
            #     result = result.replace('\n',',')
            #     covstats[job_output+"_"+sample] = result
                # for line in reversed(open(cwd+"/"+job_output+"/"+file).readlines()):
                #     match = re.compile("^--.*max\s(\d*)\sbp.*N50\s(\d*).*").search(line)
                #     if not match == None:
                #         results[job_output][sample]['max_contig'] = match.group(1)
                #         results[job_output][sample]['n50'] = match.group(2)
                #         break

# print(covstats)

# for job,smpls in results.iteritems():
#     for smpl,measures in smpls.iteritems():
#         sys.stdout.write('job,sample')
#         for key,value in measures.iteritems():
#             sys.stdout.write(","+key)
#         print('')
#         break
#     break
#
#
# for job,smpls in results.iteritems():
#     for smpl,measures in smpls.iteritems():
#         sys.stdout.write(job+","+smpl)
#         for key,value in measures.iteritems():
#             sys.stdout.write(","+str(value))
#         print('')
ale_rel = {}

for job,smpls in results.iteritems():
    for smpl,measures in smpls.iteritems():
        if not ale_rel.has_key(smpl):
            ale_rel[smpl] = []

        for key,value in measures.iteritems():
            if key == 'ALE_score':
                ale_rel[smpl].append(value)

for s,a in ale_rel.iteritems():
    print(s,min(a))
# ('V6_S3_R1_001_1P', '-370150502.129622')
# ('V1_S5_R1_001_1P', '-156223052.277216')



col = {}
i=0
for job,smpls in results.iteritems():
    for smpl,measures in smpls.iteritems():
        col[i] = {}
        col[i]['job'] = job
        col[i]['sample'] = smpl
        for key,value in measures.iteritems():
            col[i][key] = value

        if smpl == 'V6_S3_R1_001_1P':
            col[i]['ale_rel'] = float(-370150502.129622)/float(col[i]['ALE_score'])
        else:
            col[i]['ale_rel'] = float(-156223052.277216)/float(col[i]['ALE_score'])
        i+=1



df = pd.DataFrame(data=col)
df = df.transpose()
df['n50'] = df['n50'].apply(pd.to_numeric)
df['max_contig'] = df['max_contig'].apply(pd.to_numeric)
df['kstep'] = df['kstep'].apply(pd.to_numeric)
df['kmin'] = df['kmin'].apply(pd.to_numeric)
df['kmax'] = df['kmax'].apply(pd.to_numeric)
print(df)

sns.set(style="ticks", color_codes=True)

sns_plot = sns.catplot(x="sample", y="ale_rel", data=df, hue="kstep")
sns_plot.savefig("output_ale_kstep.png")
sns_plot = sns.catplot(x="sample", y="ale_rel", data=df, hue="kmin")
sns_plot.savefig("output_ale_kmin.png")
sns_plot = sns.catplot(x="sample", y="ale_rel", data=df, hue="kmax")
sns_plot.savefig("output_ale_kmax.png")
sns_plot = sns.catplot(x="sample", y="ale_rel", data=df, hue="prunelevel")
sns_plot.savefig("output_ale_prunelvel.png")
sns_plot = sns.catplot(x="sample", y="ale_rel", data=df, hue="nomercy")
sns_plot.savefig("output_ale_mercy.png")

sns_plot = sns.relplot(x="mappedFraction", y="ale_rel", data=df, hue="kmin")
sns_plot.savefig("output_mapped_kmin.png")
sns_plot = sns.relplot(x="mappedFraction", y="ale_rel", data=df, hue="kmax")
sns_plot.savefig("output_mapped_kmax.png")
sns_plot = sns.relplot(x="mappedFraction", y="ale_rel", data=df, hue="kstep")
sns_plot.savefig("output_mapped_kstep.png")
sns_plot = sns.relplot(x="mappedFraction", y="ale_rel", data=df, hue="nomercy")
sns_plot.savefig("output_mapped_nomercy.png")

sns_plot = sns.relplot(x="n50", y="ale_rel", data=df, hue="kstep")
sns_plot.savefig("output_n50_kstep.png")
sns_plot = sns.relplot(x="n50", y="ale_rel", data=df, hue="kmin")
sns_plot.savefig("output_n50_kmin.png")
sns_plot = sns.relplot(x="n50", y="ale_rel", data=df, hue="kmax")
sns_plot.savefig("output_n50_kmax.png")
sns_plot = sns.relplot(x="n50", y="ale_rel", data=df, hue="nomercy")
sns_plot.savefig("output_n50_nomercy.png")
sns_plot = sns.relplot(x="max_contig", y="ale_rel", data=df, hue="sample")
sns_plot.savefig("output_maxcontig.png")
# v6 = df.loc[df['sample'] == 'V6_R1_100000sample']
# v5 = df.loc[df['sample'] == 'V5_R1_100000sample']
# max_ale_v6 = v6['ALE_score'].max()
# max_ale_v5 = v5['ALE_score'].max()
# v6['ALE_score'] = v6['ALE_score'].apply(lambda x: x/max_ale_v6)
# v5['ALE_score'] = v5['ALE_score'].apply(lambda x: x/max_ale_v5)
# print(v6)
