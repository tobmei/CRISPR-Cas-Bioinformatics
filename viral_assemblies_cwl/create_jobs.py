#!/usr/bin/python
import argparse


parser = argparse.ArgumentParser(description="this script does the following...")

parser.add_argument('--output', help="path to output directory", required=True)
#parser.add_argument('--forward', help="forward reads", required=True)
#parser.add_argument('--reverse', help="revrese reads", required=True)

args = parser.parse_args()

output_dir = args.output
#fwd = args.forward
#rev = args.reverse


#input_string = 'R1forward:\n\
#  class: File\n\
#  path: {}\n\
#R2reverse:\n\
#  class: File\n\
#  path: {}\n'.format(fwd,rev)


##----------------#
##--MEGAHIT JOBS--#
##----------------#
asssembly_string = 'kmin: {}\n\
kmax: {}\n\
kstep: {}\n\
#megaPruneLevel: {}\n\
#megaNoMercy: {}\n\
megaNoBubble: {}\n\
#megaLowLocalRatio: {}\n\
#megaMaxTipLens: {}\n\
#megaMergeLevel: {}\n\
#megaNoLocal: {}\n\
#megaKmin1Pass: {}\n\
#megaMinCount: {}\n'
#
k_mins = [15,21,31]
k_maxs = [99,127]#,85,127]
k_steps = [10,20,28]#,30]
prune_level = [2]#,1]
no_mercy = ['false']#,'true']
bubble_lvl = [0,1,2]
low_local_ratio = [0.2]#,0.5]
max_tip_len = [2]#,1,3]
merge_level = ['[20,0.98]']#,'20,0.98']
no_local = ['false']#,'true']
kmin_1pass = ['true']#,'false']
min_count = [2]#,1,3]

i = 0
for min in k_mins:
   for max in k_maxs:
       for step in k_steps:
           for prune in prune_level:
               for mercy in no_mercy:
                   for bubble in bubble_lvl:
                       for low in low_local_ratio:
                           for tip in max_tip_len:
                               for merge in merge_level:
                                   for local in no_local:
                                       for kmin in kmin_1pass:
                                           for count in min_count:
                                               file = open('{}/job_megahit_{}.yml'.format(output_dir,i),'w')
                                               file.write(asssembly_string.format(min,max,step,prune,mercy,bubble,low,tip,merge,local,kmin,count))
                                               i+=1
                                               file.close()
                                               print("written file: {}".format(file.name))



#-------------------#
#--METASPADES JOBS--#
#-------------------#
asssembly_string = 'kList: {}\n\
#kmax: {}\n\
#kstep: {}\n\
#kmin: {}'

rrs = ['false','true']
k_mins = [15,21,31]
k_maxs = [99,127]#,85,127]
k_steps = [10,20,30]

j = 0
#for rr in rrs:
for step in k_steps:
    for min in k_mins:
        for max in k_maxs:
            list = []
            for i in range(min,max,step):
                list.append(str(i))

            s = ', '.join(list)
            file = open('{}/job_metaspades_{}.yml'.format(output_dir,j),'w')
            file.write(asssembly_string.format(s,max,step,min))
            j+=1
            file.close()
            print("written file: {}".format(file.name))





#-------------#
#--IDBA JOBS--#
#-------------#
#asssembly_string = 'kmin: {}\n\
#kmax: {}\n\
#kstep: {}\n\
#preCorrection: {}'
#
#
#k_mins = [15,21,31]
#k_maxs = [99,127]#,85,127]
#k_steps = [10,20,28]#,30]
#correction = ['false']#,'true']
#
#
#i = 0
#for min in k_mins:
#    for max in k_maxs:
#        for step in k_steps:
#            for corr in correction:
#                file = open('{}/job_idbaud_{}.yml'.format(output_dir,i),'w')
#                file.write(input_string + asssembly_string.format(min,max,step,corr))
#                i+=1
#                file.close()
#                print("written file: {}".format(file.name))