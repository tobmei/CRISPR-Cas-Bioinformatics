#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 13:57:47 2019

@author: tobias
"""

import argparse
import os
import sys
import glob
import re
import subprocess
import time
import multiprocessing


parser = argparse.ArgumentParser(description="this script does the following...")

parser.add_argument('--jobdir', help="path to directory with job files", required=True)
parser.add_argument('--workflowdir', help="path to workflow directory", required=True)
parser.add_argument("--output", help="output directory", required=True)


args = parser.parse_args()

#parser.print_help()

#Assuming job files named job_<assembler>_<nr>.yml
print(args)
jobdir_path = args.jobdir
output = args.output
tmpdir_prefix = "tmeiercwl"
workflow_dir = args.workflowdir

job_pattern = re.compile("job_(.*)_(\d*)")

result_list = []
job_files = {}

if not os.path.exists(jobdir_path):
    sys.exit("jobdir path {} not found".format(jobdir_path))


#create output directory
if not os.path.exists(output):
    os.system("mkdir {}".format(output))
    
    
def cwl_runner(job_file):
    start = time.time()
    subprocess.call(['cwltool',\
#                                    '--verbose',\
                                "--quiet",\
#                                    "--parallel",\
                                "--outdir",\
                                cur_job_dir,\
                                "--tmp-outdir-prefix",\
                                "/tmp/{}".format(tmpdir_prefix),\
                                "--tmpdir-prefix",\
                                tmpdir_prefix,\
                                workflow_file,\
                                job_file])
    end = time.time()
    runtime = end-start
    print("cwl runtime: {}".format(runtime))    
    
    #cleaning up
    print("cleaning...")
    print("command: rm -rf /tmp/{}*".format(tmpdir_prefix))
    print("command: rm -rf {}/{}*".format(output,tmpdir_prefix))
    os.system("rm -rf /tmp/{}*".format(tmpdir_prefix))
    os.system("rm -rf {}/{}*".format(cur_job_dir,tmpdir_prefix))


def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)
    
def multi(job_files,cur_job_dir):
    pool = multiprocessing.Pool(processes=8)
    for file in job_files:
        pool.apply_async(cwl_runner, args=(file,), callback=log_result)
    pool.close()
    pool.join()
    print(result_list)
    
#iterate over each job file
for job_file in glob.glob("{}/job_*.yml".format(jobdir_path)):
    assembler = job_pattern.search(job_file).group(1)
    job_nr = job_pattern.search(job_file).group(2)
    cur_job_dir = "{}/{}/{}".format(output,assembler,job_nr)
    
    os.chdir(output)
    
    workflow_file = "{}workflow_{}.cwl".format(workflow_dir,assembler)
    if not os.path.isfile(workflow_file):
        sys.exit("workflow file {} not found".format(workflow_file))
    
    #create job output directory
    if not os.path.exists("{}/{}".format(output,assembler)): #output/megahit?
        os.system("mkdir {}/{}".format(output,assembler))
        
    os.system("mkdir {}".format(cur_job_dir)) #ouput/assembler/1
    os.chdir(cur_job_dir) #change to job directory where cwltool should be executed   
    
    #execute cwltool command
    print("running cwltool...")
    print("Workflow: {}".format(workflow_file))
    print("job: {}".format(job_file))
    print("Assembler: {}".format(assembler))
    print("job nr: {}".format(job_nr))

    subprocess.call(['cwltool',\
#                                    '--verbose',\
                                "--quiet",\
#                                    "--parallel",\
                                "--outdir",\
                                cur_job_dir,\
                                "--tmp-outdir-prefix",\
                                "/tmp/{}".format(tmpdir_prefix),\
                                "--tmpdir-prefix",\
                                tmpdir_prefix,\
                                workflow_file,\
                                job_file])
    
    
    #cleaning up
    print("cleaning...")
    print("command: rm -rf /tmp/{}*".format(tmpdir_prefix))
    print("command: rm -rf {}/{}*".format(output,tmpdir_prefix))
    os.system("rm -rf /tmp/{}*".format(tmpdir_prefix))
    os.system("rm -rf {}/{}*".format(cur_job_dir,tmpdir_prefix))
    



