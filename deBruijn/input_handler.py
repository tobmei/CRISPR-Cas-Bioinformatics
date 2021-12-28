import sys
import os.path


def input_k(inp):
    k = 0
    # if non-convertable to int format is entered
    # exit the system
    try:
        k = int(inp)
    except Exception:
        print("Please enter integer for -k terminal argument")
        sys.exit()
    return k

def input_in_file(inp):
    # check if file exists under input
    # else exit system
    input = inp if "input/" in inp else "input/"+inp
    if os.path.isfile(input):
        file = input
        return file
    else:
        print("Please check whether input file exists!")
        sys.exit()
