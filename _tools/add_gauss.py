import count_black
import tool_gauss
import os
import glob
import shutil
import argparse
import config

import numpy as np

# the input folder name where we look up the names of the respective inputs
# this should be in your "*_train" folder besides the maskDir directory
# Assumes that you have different folder for the gauss masks and the input masks
input_folder_name = "input_filtered"

def copy_file(image_name):
        shutil.copyfile(
        os.path.join(config.maskDir, "0001.png"),
        os.path.join(config.maskDir, image_name)
    )

def copy_masks_to_gauss(s):
    input_path = "input_gdisko_gauss_r10_s10" if s== 10 else "input_gdisko_gauss_r10_s15"
    mask_source_path = config.gdisko_gauss_r10_s10_dir if s == 10 else config.gdisko_gauss_r10_s15_dir

    # get train_path 
    # assumes that maskDir is in *_train
    train_path = os.path.dirname(config.maskDir)
    train_masks_path = os.path.join(train_path, input_path)

    # create folder for training_masks if it does not exists
    if not os.path.exists(train_masks_path):
        os.mkdir(train_masks_path)

    # clear previous masks
    previous_masks = os.path.join(train_masks_path, "*.png")
    file_list = glob.glob(previous_masks)
    for f in file_list:
        os.remove(f)
    
    # copy masks to train folder
    input_filenames = map(os.path.basename, glob.glob(os.path.join(train_path, input_folder_name, "*.png")))
    for file in input_filenames:
        source_mask_path = os.path.join(mask_source_path, file)
        if os.path.isfile(source_mask_path):
            shutil.copy(source_mask_path, os.path.join(train_masks_path, file))

def loop(threshold, s, copy_function=copy_file, individual_zero=None, iterations=None):
    t = 1.0
    threshold /= 100.0
    step = 0
    while(True):
        if iterations is not None and step >= iterations:
            break

        # create commands with new set of gauss images
        commands = tool_gauss.create_commands()

        # either s10 or s15
        if(s==10):
            command = commands[0]
            gauss_dir = config.gdisko_gauss_r10_s10_dir
        else:
            command = commands[1]
            gauss_dir = config.gdisko_gauss_r10_s15_dir

        # compute the gauss images
        os.system(command)

        # count the number of black pixels
        # adjust them to the mask size if provided
        image_name, t = count_black.go_through_images(gauss_dir, individual_zero)

        # exit if threshold is small enough
        # copy masks into train folder and exit
        if(t < threshold) and iterations is not None:
            copy_masks_to_gauss(s)
            break

        # create a new gauss-mask at the position with the most black pixels
        copy_function(image_name)
        step += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Counts the number of black pixels in images contained in input_gdisko_gauss_r10_s*
    It looks for the image with the highest number of black pixels and adds a new mask at that position. It repeats that process until a certain threshold is reached
    This script assumes that there exists already a mask with name "0001.png". Change that name to w/e you like in the script.
    """)

    parser.add_argument("--threshold", "-t",
        help="The threshold when to stop in percent",
        required=True,
        type=float
    )

    parser.add_argument("-s",
        help="Whether to optimize *_s10 or *_s15",
        default=10,
        type=int
    )

    parser.add_argument("--iterations", "-i",
        type=int
    )

    args = parser.parse_args()
    loop(args.threshold, args.s, iterations=args.iterations)