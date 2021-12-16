#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser(description="this script does the following...")

parser.add_argument('--output', help="path to output directory", required=True)
# parser.add_argument('--forward', help="forward reads", required=True)
# parser.add_argument('--reverse', help="revrese reads", required=True)

args = parser.parse_args()

output_dir = args.output
# fwd = args.forward
# rev = args.reverse


# input_string = 'R1forward:\n\
#  class: File\n\
#  path: {}\n\
# R2reverse:\n\
#  class: File\n\
#  path: {}\n'.format(fwd,rev)


##----------------#
##--MEGAHIT JOBS--#
##----------------#
asssembly_string = 'kmin {}\nkmax {}\nkstep {}\nprunelevel {}\nbubble {}\ncleaningrounds {}'
#
# k_mins = [25, 35]
# k_maxs = [95, 145]
# k_steps = [10, 20]
# prune_level = [0, 1, 2, 3]
# bubble_lvl = [0, 1, 2]
# cleaning_rounds = [1, 2, 3, 4, 5]
# k_mins = [25]
# k_maxs = [145]
# k_steps = [10]
#
# i = 0
# for min in k_mins:
#     for max in k_maxs:
#         for step in k_steps:
#             for prune in prune_level:
#                 for bubble in bubble_lvl:
#                     for cl in cleaning_rounds:
#                         file = open('{}/{}'.format(output_dir, i), 'w')
#                         file.write(asssembly_string.format(min, max, step, prune, bubble, cl))
#                         i += 1
#                         file.close()
#                         print("written file: {}".format(file.name))

# -------------------#
# --METASPADES JOBS--#
# -------------------#
asssembly_string = ''

k_mins = [25]
k_maxs = [128]
k_steps = [10]

j = 0
for step in k_steps:
    for min in k_mins:
        for max in k_maxs:
            list = []
            for i in range(min,max+step,step):
                if i<128:
                    list.append(str(i))

            s = ', '.join(list)
            file = open('{}/{}'.format(output_dir,j),'w')
            file.write(s)
            j+=1
            file.close()
            print("written file: {}".format(file.name))


# -------------#
# --IDBA JOBS--#
# -------------#
# asssembly_string = 'kmin: {}\n\
# kmax: {}\n\
# kstep: {}\n\
# preCorrection: {}'
#
#
# k_mins = [15,21,31]
# k_maxs = [99,127]#,85,127]
# k_steps = [10,20,28]#,30]
# correction = ['false']#,'true']
#
#
# i = 0
# for min in k_mins:
#    for max in k_maxs:
#        for step in k_steps:
#            for corr in correction:
#                file = open('{}/job_idbaud_{}.yml'.format(output_dir,i),'w')
#                file.write(input_string + asssembly_string.format(min,max,step,corr))
#                i+=1
#                file.close()
#                print("written file: {}".format(file.name))