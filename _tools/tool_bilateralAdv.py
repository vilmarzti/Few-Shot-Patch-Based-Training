import os
import multiprocessing as mp
import config

os.makedirs(os.path.dirname(config.outputFormat),exist_ok=True)

def create_command(frame):
  return "./bilateralAdv/bilateralAdv "+ config.imageFormat+" " + config.flowFwdFiles+" " + config.flowBwdFiles+(" %d "%(frame))+" 15 16 "+(outputFormat%(frame))

firstFrame = int(config.frameFirst)
lastFrame= int(config.frameLast)

commands = [create_command(frame) for frame in range(firstFrame, lastFrame + config.frameStep, config.frameStep)]

pool = mp.Pool(mp.cpu_count())
pool.map(os.system, commands)
