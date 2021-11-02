import os
import multiprocessing as mp

################ MAKE CHANGES HERE #################
inputFileFormat = "%04d"            # name of input files, e.g., %03d if files are named 001.png, 002.png
imageFormat   = "../TEST_DATA/bf_gen/input/" + inputFileFormat + ".png"
flowFwdFormat = "../TEST_DATA/bf_gen/flow_fwd/" + inputFileFormat + ".A2V2f"  # path to the forward flow files (computed by _tools/disflow)
flowBwdFormat = "../TEST_DATA/bf_gen/flow_bwd/" + inputFileFormat + ".A2V2f"  # path to the backward flow files (computed by _tools/disflow)
outputFormat  = "../TEST_DATA/bf_gen/input_filtered/" + inputFileFormat + ".png"  # path to the result filtered sequence
frameFirst = 1                      # number of the first PNG file in the input folder
frameLast = 1417                    # number of the last PNG file in the input folder
num_cores = mp.cpu_count()
####################################################

os.makedirs(os.path.dirname(outputFormat),exist_ok=True)

def create_command(frame):
  return "bilateralAdv.exe "+imageFormat+" "+flowFwdFormat+" "+flowBwdFormat+(" %d "%(frame))+" 15 16 "+(outputFormat%(frame))

firstFrame = frameFirst
lastFrame= frameLast  
frameStep = +1

commands = [create_command(frame) for frame in range(firstFrame, lastFrame + frameStep, frameStep)]

pool = mp.Pool(num_cores)
pool.map(os.system, commands)
