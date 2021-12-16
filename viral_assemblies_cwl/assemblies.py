#!/usr/bin/python
import subprocess
import os
import re
import numpy as np
import sys
import shlex

home = "/home/tmeier"
ale = home+"/ALE/src"
idba = home+"/idba-master/bin"
megahit = "/tools/bin"
metaSpades = home+"/SPAdes-3.13.0-Linux/bin"
dna1 = home+"/medamcan/bioreaktor/BGR_DNA_141119_S0_L000_R1_000_val_1.fastq"
dna2 = home+"/medamcan/bioreaktor/BGR_DNA_141119_S0_L000_R2_000_val_2.fastq"
vdna1 = home+"/medamcan/bioreaktor/BGR_vDNA_viral_S0_L000_R1_000_val_1.fastq"
vdna2 = home+"/medamcan/bioreaktor/BGR_vDNA_viral_S0_L000_R1_000_val_2.fastq"
dna1_prepro = home+"/medamcan/bioreaktor/prepro/good_DNA_1.fastq"
dna2_prepro = home+"/medamcan/bioreaktor/prepro/good_DNA_2.fastq"
vdna1_prepro = home+"/medamcan/bioreaktor/prepro/vDNA_good_1.fastq"
vdna2_prepro = home+"/medamcan/bioreaktor/prepro/vDNA_good_2.fastq"
#vdna1_prepro = home+"/medamcan/bioreaktor/prepro/vDNA_good_1_subsample.fastq"
#vdna2_prepro = home+"/medamcan/bioreaktor/prepro/vDNA_good_2_subsample.fastq"
vdna_merged = home+"/medamcan/bioreaktor/prepro/vDNA_good_merged.fa"

assembly_dir = home+"/medamcan/bioreaktor/assembly/viral/prepro"
#assembly_dir = home+"/medamcan/bioreaktor/assembly/viral/test"
out_megahit = assembly_dir+"/megahit"
out_metaspades = assembly_dir+"/metaspades"
out_idba = assembly_dir+"/idba"

#prepro prinseq-lite
#-fastq medamcan/bioreaktor/BGR_vDNA_viral_S0_L000_R1_000_val_1.fastq
#-fastq2 medamcan/bioreaktor/BGR_vDNA_viral_S0_L000_R2_000_val_2.fastq
#-out_good medamcan/bioreaktor/prepro/vDNA_good
#-out_bad medamcan/bioreaktor/prepro/vDNA_bad
#-no_qual_header
#-min_len 80
#-trim_to_len 120
#-lc_method entropy
#-lc_threshold 70
#-trim_qual_right 25
#-trim_qual_type mean
#-trim_qual_window 5
#-trim_qual_step 5
#-stats_all > medamcan/bioreaktor/prepro/stats_all

def run_assemblies():
    #run megahit
    base = ["{}/megahit".format(megahit),"-1", vdna1_prepro, "-2", vdna2_prepro]
    default   = ["--min-count", "2", "--k-min", "21", "--k-max", "99", "--k-step", "20", "-o", out_megahit+"_default"]
    sensitive = ["--min-count", "2", "--k-min", "21", "--k-max", "99", "--k-step", "10", "-o", out_megahit+"_sensitive"]
    smallk = ["--min-count", "2", "--k-min", "15", "--k-max", "99", "--k-step", "10", "-o", out_megahit+"_smallk"]
    presets = [default, sensitive]#, smallk]
    for pre in presets :
        megahit_cmd = base + pre
        #proc = subprocess.call(megahit_cmd)

    #run metaSpades
    base = ["{}/./spades.py".format(metaSpades), "--meta", "-1", vdna1_prepro, "-2", vdna2_prepro, "-t", "48"]
    default   = ["-k", "21,41,61,71,91", "-o", out_metaspades+"_default"]
    sensitive = ["-k", "21,31,41,51,61,71,81,91", "-o", out_metaspades+"_sensitive"]
    presets = [default, sensitive]
    for pre in presets :
        metaspades_cmd = base + pre
        proc = subprocess.call(metaspades_cmd)

    #run idba_ud
    base =[idba+"/idba_ud", "-r", vdna_merged]
    default = ["--step", "20", "--mink", "20", "--maxk", "100", "-o", out_idba+"_default"]
    sensitive = ["--step", "10", "--mink", "20", "--maxk", "100", "-o", out_idba+"_sensitive"]
    no_bubble = ["--step", "20", "--mink", "20", "--maxk", "100", "--no_bubble", "-o", out_idba+"_no_bubble"]
    pre_correction = ["--step", "20", "--mink", "20", "--maxk", "100", "--pre_correction", "-o", out_idba+"_pre_correction"]
    presets = [sensitive, no_bubble, pre_correction]#, default]
    for pre in presets :
        idba_cmd = base + pre
        proc = subprocess.call(idba_cmd)

##evaluation

#contig statistics
#read backmapping, coverage

#ass_dirs = [x[2] for x in os.walk(assembly_dir)]
#print ass_dirs
#iterate over evrey contig file and calculate stats
def contig_stats():
    ale_stats = {}
    r = re.compile("(final.)?contigs?\.fa(sta)?$")
    for folder in os.listdir(assembly_dir) :
        if not re.compile("megahit").match(folder):
            continue
        contig_file = [fn for fn in os.listdir(assembly_dir+"/"+folder) if r.match(fn)][0]
        contig_path = assembly_dir+"/"+folder+"/"+contig_file
        assembly_method = folder
        assembly_meth_dir = assembly_dir+"/"+folder
        print(assembly_method+" contigs path: " +contig_path)


        # command = "|".join([
        #                 "bwa mem {}/index {} {}".format(assembly_meth_dir, vdna1_prepro_sub, vdna2_prepro_sub),
        #                 "samtools flagstat -",
        #                 "awk 'FNR==5{print $5}'",
        #                 "grep -o [0-9]*.[0-9]*"
        #                 ])
        # pipeline = ProcessPipeline(command)
        # if not pipeline.run():
        #     print "ERROR: Pipeline failed"
        # else:
        #     print "output: "+pipeline.output

        #read mapping to bam
        #create bwa index, move files to assembly dir and run bwa mem
        # subprocess.Popen(["bwa", "index", "-p", "index", contig_path]).wait()
        # subprocess.Popen(["mv -f -t {} index.*".format(assembly_meth_dir)], shell=True).wait()
        # subprocess.Popen(["bwa mem {}/index {} {} > {}/mapping.bam".format(assembly_meth_dir,vdna1_prepro,vdna2_prepro,assembly_meth_dir)], shell=True).wait()

        #subprocess.Popen(["bowtie2-build", contig_path, "index"]).wait()
        # subprocess.Popen(["mv -f -t {} index.*".format(assembly_meth_dir)], shell=True).wait()
        # bowtie2 = subprocess.Popen(["bowtie2", "--very-sensitive", "--threads", "48", "-x", assembly_meth_dir+"/index", "-1", vdna1_prepro, "-2" ,vdna2_prepro], stdout=subprocess.PIPE)
        # subprocess.Popen(["samtools view -b - > {}/mapping.bam".format(assembly_meth_dir)], stdin=bowtie2.stdout, shell=True).wait()

        #run samtools flagstat and grep number of mapped reads
        #samt_view = subprocess.Popen(["samtools view", "-c", "-F", "0x4"], stdin=bwa_mem.stdout, stdout=subprocess.PIPE)
        samt_falgstat = subprocess.Popen(["samtools", "flagstat", assembly_meth_dir+"/mapping.bam"], stdout=subprocess.PIPE)
        awk_mapped = subprocess.Popen(["awk", "FNR==5{print}"], stdin=samt_falgstat.stdout, stdout=subprocess.PIPE)
        grep = subprocess.Popen(["grep", "-o", "[0-9]*\.[0-9]*"], stdin=awk_mapped.stdout, stdout=subprocess.PIPE)
        nr_mapped_reds = grep.communicate()[0].strip("\n")

        #run samtools depth to get the average depth and breath of coverage
        samt_sort = subprocess.Popen(["samtools", "sort", assembly_meth_dir+"/mapping.bam"], stdout=subprocess.PIPE)
        samt_depth = subprocess.Popen(["samtools", "depth", "-a", "-"], stdin=samt_sort.stdout, stdout=subprocess.PIPE)
        awk_mean_depth = subprocess.Popen(["awk", "{c++;s+=$3} END {print s/c}"], stdin=samt_depth.stdout, stdout=subprocess.PIPE)
        awk_cov_breath = subprocess.Popen(["awk", "{c++;if($3>0)total++} END {print (total/c)*100}"], stdin=samt_depth.stdout, stdout=subprocess.PIPE)
        out_cov_breath = awk_cov_breath.communicate()[0].strip("\n")
        out_mean_depth = awk_mean_depth.communicate()[0].strip("\n")

        #run ale
        ale_cmd = subprocess.Popen([ale+"/ALE", "--metagenome", assembly_meth_dir+"/mapping.bam", contig_path, assembly_meth_dir+"/ALEoutput.txt"]).wait()
        ale_stats[assembly_method] = {}
        with open(assembly_meth_dir+"/ALEoutput.txt") as ale_file:
            for line in ale_file:
                if not re.compile("^#").match(line):
                    break
                else:
                    line = shlex.split(line)
                    ale_stats[assembly_method][line[1].strip(":")] = line [2]

        #contig stats
        contig_len = []
        total_len = 0
        gc = 0.0
        with open(contig_path) as cntgs_file:
            for line in cntgs_file :
                if not (re.compile(">").match(line)):
                    contig_len.append(len(line.strip("\n")))
                    total_len += len(line.strip("\n"))
                    gc += line.count("G") + line.count("C")

        gc_cont = (gc/total_len)*100
        stats = {}
        stats["mean_depth"] = out_mean_depth
        stats["breath_cov"] = out_cov_breath
        stats["mapped_reads"] = nr_mapped_reds
        seq_array = np.array(contig_len)
        stats['sequence_count'] = seq_array.size
        stats['gc_content'] = round(gc_cont,2)
        sorted_lens = seq_array[np.argsort(-seq_array)]
        stats['longest'] = int(sorted_lens[0])
        stats['shortest'] = int(sorted_lens[-1])
        stats['median'] = np.median(sorted_lens)
        stats['mean'] = round(np.mean(sorted_lens), 2)
        stats['total_bps'] = int(np.sum(sorted_lens))
        csum = np.cumsum(sorted_lens)
        nx = int(stats['total_bps'] * 0.5)
        csumn = min(csum[csum >= nx])
        l_level = int(np.where(csum == csumn)[0])
        n_level = int(sorted_lens[l_level])
        stats["N50"] = n_level
        print(stats)

    #print ale stats in long format
    ale_file = open(assembly_dir+"/ale_summary.txt", "a")
    ale_file.write("assembly_method,key,value\n")
    for k,v in ale_stats.items():
        #print "key: "+k
        for i in v.items():
            ale_file.write(k+","+i[0]+","+i[1]+"\n")
    ale_file.close()


class ProcessPipeline(object):
    def __init__(self,command):
        self.command = command
        self.command_list = command.split("|")
        self.output = None
        self.errs = None
        self.status = None
        self.result = None

    def run(self):
        process_list = list()
        prev_process = None
        for command in self.command_list:
            args = shlex.split(command)
            if(prev_process is None):
                process = subprocess.Popen(args, stdout=subprocess.PIPE)
            else:
                process = subprocess.Popen(args, stdin=prev_process.stdout, stdout=subprocess.PIPE)
            process_list.append(process)
            prev_process = process
        last_process = process_list[-1]
        self.output, self.errs = last_process.communicate()
        self.status = last_process.returncode
        self.result = (self.status == 0)
        return self.result


if __name__ == "__main__":
    #run_assemblies()
    contig_stats()
