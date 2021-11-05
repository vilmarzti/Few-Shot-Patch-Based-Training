import count_black
import tool_gauss
import os
import shutil
import argparse

def loop(threshold, s):
    t = 1.0
    threshold /= 100.0

    while(True):
        # create commands with new set of gauss images
        commands = tool_gauss.create_commands()

        # either s10 or s15
        if(s==10):
            command = commands[0]
            gauss_dir = tool_gauss.gdisko_gauss_r10_s10_dir
        else:
            command = commands[1]
            gauss_dir = tool_gauss.gdisko_gauss_r10_s15_dir

        # compute the gauss images
        os.system(command)

        # count the number of black pixels
        image_name, t = count_black.go_through_images(gauss_dir)

        # exit if threshold is small enough
        if(t < threshold):
            break

        # create a new gauss-mask at the position with the most black pixels
        shutil.copyfile(
            os.path.join(tool_gauss.maskDir, "0001.png"),
            os.path.join(tool_gauss.maskDir, image_name)
        )


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

    args = parser.parse_args()
    loop(args.threshold, args.s)