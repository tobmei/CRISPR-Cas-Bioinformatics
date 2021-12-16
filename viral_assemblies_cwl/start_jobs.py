#!/usr/bin/python

import os
import glob
import re

job_dir = '/home/tmeier/medamcan/ref_assemblies/jobs'
megahit_workflow = '/home/tmeier/medamcan/ref_assemblies/pipeline/workflow_scatter_megahit.cwl'
pattern = re.compile("(job_megahit_\d*)")
cwd = os.getcwd()

for job_file in glob.glob('{}/job_megahit_*.yml'.format(job_dir)):
    job_name = pattern.search(job_file).group(1)
    if os.path.exists(cwd+"/"+job_name):
        print("path exists: "+cwd+"/"+job_name)
        continue
    # else:
    #     print("path does not exists: "+cwd+"/"+job_name)
    #     continue


    # create job folders
    os.system('mkdir {}'.format(job_name))
    cur_job_dir = '{}/{}'.format(cwd,job_name)
    print('created directory: {}'.format(cur_job_dir))
    #change cwd to current job directory (e.g. job_megahit_1)
    os.chdir(cur_job_dir)
    #run workflow with current job_file in cur_job_dir
    print('running workflow with job_file: {}'.format(job_file))
    print('command: cwltool --debug {} {} &> {}.workflow.log'.format(megahit_workflow,job_file,job_name))
    os.system('cwltool --debug {} {} &> {}.workflow.log'.format(megahit_workflow,job_file,job_name))
    os.chdir(cwd)
