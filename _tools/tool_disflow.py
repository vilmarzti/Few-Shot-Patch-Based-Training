import os
import multiprocessing as mp

################ MAKE CHANGES HERE #################
inputDir = "/home/martin/Videos/ondrej_et_al/bf/bf_gen/input_filtered/"              # path to the input sequence PNGs
inputFileFormat = "%04d"        # name of input files, e.g., %03d if files are named 001.png, 002.png
inputFileExt = "png"            # extension of input files (without .), e.g., png, jpg
flowFwdDir = "../TEST_DATA/bf_gen/flow_fwd"         # path to the output forward flow files
flowBwdDir = "../TEST_DATA/bf_gen/flow_bwd"         # path to the output backward flow files
FIRST = 1                       # number of the first PNG file in the input folder
LAST = 1417                      # number of the last PNG file in the input folder
num_cores = mp.cpu_count()
####################################################


if not os.path.exists(flowFwdDir):
    os.mkdir(flowFwdDir)
    
if not os.path.exists(flowBwdDir):
    os.mkdir(flowBwdDir)

inputFiles = inputDir + "/" + inputFileFormat + "." + inputFileExt
flwFwdFile = flowFwdDir + "/" + inputFileFormat + ".A2V2f"
flwBwdFile = flowBwdDir + "/" + inputFileFormat + ".A2V2f"

def create_commands(frame, fwd=True):
  if fwd:
    command = "./disflow/disflow %s %s %s"%(inputFiles%(frame),inputFiles%(frame-frameStep),flwFwdFile%(frame)) 
  else:
    command = "./disflow/disflow %s %s %s"%(inputFiles%(frame),inputFiles%(frame-frameStep),flwBwdFile%(frame)) 
  return command

pool = mp.Pool()

firstFrame = FIRST+1
lastFrame  = LAST
frameStep  = +1

fwd_commands = [create_commands(frame) for frame in range(firstFrame, lastFrame + frameStep, frameStep)]
pool.map(os.system, fwd_commands)

firstFrame = LAST-1
lastFrame  = FIRST
frameStep  = -1

bwd_commands = [create_commands(frame, False) for frame in range(firstFrame, lastFrame + frameStep, frameStep)]
pool.map(os.system, bwd_commands)