#!/usr/bin/env python3

import argparse
import glob
import re
import multiprocessing
import logging
import sys
import os
import statistics
import random

# initialize argument parser
parser = argparse.ArgumentParser(description="this is one awesome script")
parser.add_argument("--input", help="path to input directory with DATA_* files", required=True)
args = parser.parse_args()
input_dir = args.input

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(screen_handler)


def get_trajectory(first, second, third):
    if first == 1 and second == 2 and third == 1:
        return 'a'
    elif first == 1 and second == 2 and third == 3:
        return 'b'
    elif first == 3 and second == 2 and third == 3:
        return 'c'
    elif first == 3 and second == 2 and third == 1:
        return 'd'
    elif first == 2 and second == 1 and third == 2:
        return 'e'
    elif first == 2 and second == 3 and third == 2:
        return 'f'
    else:
        return 'x'


def classify_glucose(glucose):
    q = glucose / (glucose + magic_number)
    if q > qse:
        return 3
    if q < qss:
        return 1
    return 2


def all_in_one():
    data_dict = {}

    data_files = [x for x in glob.glob("{}/DATA_000001*".format(input_dir))]
    data_files.sort()
    previous_glucose = 0

    is_first_file = True

    number_of_timepoints = 0
    randoms_chosen = False

    for data_file in data_files:
        logging.info("processing: {}".format(data_file))
        # timepoint = float(re.search(".*DATA_([0-9]*)", data_file).group(1))
        # timepoint *= 0.01
        # timepoint = round(timepoint, 2)
        number_of_timepoints += 1

        if data_file == data_files[-1]:
            is_last_file = True
        else:
            is_last_file = False

        # if its not the first file, i.e. all particles are in the dictionary
        # choose 20 random particles
        if not is_first_file:
            if not randoms_chosen:
                random_particles = random.sample(list(data_dict), 20)
                randoms_chosen = True

        with open(data_file, "r") as inp:
            for line in inp:

                line_split = line.split("\t")
                if line_split[0] == "ID":  # skip header
                    continue

                particle_id = line_split[0]
                if len(line_split) < 6:
                    logging.info("something is not right in {} for particle {}... skipping this one".format(data_file,particle_id))
                    continue
                glu = float(line_split[1])
                oxy = line_split[2]

                # if glucose is zero, use value from previous time point
                if glu == 0.0:
                    if previous_glucose > 0:
                        trans_gl = classify_glucose(previous_glucose)
                else:
                    trans_gl = classify_glucose(glu)
                previous_glucose = glu


                # initialize data_dict
                if is_first_file:
                    data_dict[particle_id] = [ [], [], [], [], [], [], [], [], [] ]

                translated_glucose = data_dict[particle_id][0]
                shrinked_values = data_dict[particle_id][1]
                traja = data_dict[particle_id][2]
                trajb = data_dict[particle_id][3]
                trajc = data_dict[particle_id][4]
                trajd = data_dict[particle_id][5]
                traje = data_dict[particle_id][6]
                trajf = data_dict[particle_id][7]

                random_oxy = data_dict[particle_id][8]

                # if its the first file, save oxygen for all particles
                if is_first_file:
                    random_oxy.append(oxy)
                # if its not the first file, check if current particle is a chosen one
                # save oxygen for chosen one
                if not is_first_file:
                    if particle_id in random_particles:
                        random_oxy.append(oxy)


                translated_glucose.append(trans_gl)

                # check if translated values can be shrinked
                # i.e. is first value different from last value in translated_glucose
                if len(translated_glucose) > 1:
                    if not translated_glucose[0] == translated_glucose[-1]:
                        # remove last item from list
                        last_item = translated_glucose.pop()
                        # get translated value and number of time points
                        trans_value = translated_glucose[0]
                        timepoints_count = len(translated_glucose)
                        shrinked_values.append((trans_value,timepoints_count))
                        # clear the list and insert last_item
                        translated_glucose.clear()
                        translated_glucose.append(last_item)

                # if last file, flush all the values regardless
                if is_last_file:
                    trans_value = translated_glucose[0]
                    timepoints_count = len(translated_glucose)
                    shrinked_values.append((trans_value,timepoints_count))

                # check if trajectories can be determined from shrinked_values
                # i.e. are there 4 values present
                if len(shrinked_values) == 3:
                    # get trajectory from first 3 values
                    traj = get_trajectory(shrinked_values[0][0],shrinked_values[1][0],shrinked_values[2][0])
                    time_for_traj = shrinked_values[1][1]
                    # remove first value in shrinked_values
                    shrinked_values.pop(0)
                    # add number of timepoints for traj to trajx
                    if traj == 'a': traja.append(time_for_traj)
                    elif traj == 'b': trajb.append(time_for_traj)
                    elif traj == 'c': trajc.append(time_for_traj)
                    elif traj == 'd': trajd.append(time_for_traj)
                    elif traj == 'e': traje.append(time_for_traj)
                    elif traj == 'f': trajf.append(time_for_traj)

        is_first_file = False

    return data_dict, number_of_timepoints


def write_trajectories(data_dict):
    a=[]
    b=[]
    c=[]
    d=[]
    e=[]
    f=[]
    alla = []
    allb = []
    allc = []
    alld = []
    alle = []
    allf = []

    filea = open("{}/out/trajectories_a".format(input_dir), "a")
    fileb = open("{}/out/trajectories_b".format(input_dir), "a")
    filec = open("{}/out/trajectories_c".format(input_dir), "a")
    filed = open("{}/out/trajectories_d".format(input_dir), "a")
    filee = open("{}/out/trajectories_e".format(input_dir), "a")
    filef = open("{}/out/trajectories_f".format(input_dir), "a")

    with open("{}/out/trajectories".format(input_dir), "w") as out_file:
        out_file.write("ID\ta\tb\tc\td\te\tf\n")
        for id, values in data_dict.items():
            trajsa = values[2]
            for tr in trajsa:
                filea.write(str(tr)+"\n")
            trajsb = values[3]
            for tr in trajsb:
                fileb.write(str(tr)+"\n")
            trajsc = values[4]
            for tr in trajsc:
                filec.write(str(tr)+"\n")
            trajsd = values[5]
            for tr in trajsd:
                filed.write(str(tr)+"\n")
            trajse = values[6]
            for tr in trajse:
                filee.write(str(tr)+"\n")
            trajsf = values[7]
            for tr in trajsf:
                filef.write(str(tr)+"\n")
            meana = 0 if len(trajsa) == 0 else statistics.mean(trajsa)
            meanb = 0 if len(trajsb) == 0 else statistics.mean(trajsb)
            meanc = 0 if len(trajsc) == 0 else statistics.mean(trajsc)
            meand = 0 if len(trajsd) == 0 else statistics.mean(trajsd)
            meane = 0 if len(trajse) == 0 else statistics.mean(trajse)
            meanf = 0 if len(trajsf) == 0 else statistics.mean(trajsf)
            a.append(meana)
            b.append(meanb)
            c.append(meanc)
            d.append(meand)
            e.append(meane)
            f.append(meanf)
            out_file.write(id+"\t"+str(meana)+"\t"+str(meanb)+"\t"+str(meanc)+"\t"+str(meand)+"\t"+str(meane)+"\t"+str(meanf)+"\n")

        out_file.write("average\t"+str(statistics.mean(a))+"\t"+str(statistics.mean(b))+"\t"+str(statistics.mean(c))+"\t"+
                       str(statistics.mean(d))+"\t"+str(statistics.mean(e))+"\t"+str(statistics.mean(f)))

    filea.close()
    fileb.close()
    filec.close()
    filed.close()
    filee.close()
    filef.close()


def write_oxygen(data_dict, tps):
    # generate header
    h = "particel_ID"
    for i in range(1, tps+1):
        step = float(i)*0.01
        h += "\t{}".format(str(step))
    with open("{}/out/random_oxygen".format(input_dir), "w") as out_file:
        out_file.write(h+"\n")
        for id,values in data_dict.items():
            if len(values[8]) > 1:  # i.e. chosen one
                out_file.write(id+"\t".join(values[8])+"\n")



if __name__ == "__main__":
    qse = 0.2
    qss = 0.05
    magic_number = 0.000667

    data, timepoints = all_in_one()

    logger.info("write trajectories...")
    write_trajectories(data)

    logger.info("write oxygen...")
    write_oxygen(data,timepoints)

    logger.info("all done!")
