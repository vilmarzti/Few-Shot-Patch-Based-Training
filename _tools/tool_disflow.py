import os
import multiprocessing as mp
import config

FIRST = int(config.frameFirst)                      # number of the first PNG file in the input folder
LAST = int(config.frameLast)
num_cores = mp.cpu_count()
command_string = config.disflowExecutable + " %s %s %s"

if not os.path.exists(config.flowFwdDir):
    os.mkdir(config.flowFwdDir)
    
if not os.path.exists(config.flowBwdDir):
    os.mkdir(config.flowBwdDir)

def create_commands(frame, fwd=True):
  if fwd:
    command = command_string % (config.outputFormat%(frame), config.outputFormat % (frame-frameStep), config.flowFwdFiles % (frame)) 
  else:
    command = command_string % (config.outputFormat%(frame), config.outputFormat % (frame-frameStep), config.flowBwdFiles%(frame)) 
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