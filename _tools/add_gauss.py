import count_black
import tool_gauss
import os
import shutil
import argparse

def loop(threshold):
    t = 100
    while(t > threshold):
        os.system(tool_gauss.commands[0])
        image_name, t = count_black.go_through_images(tool_gauss.maskDir)
        shutil.copyfile(os.path.join(tool_gauss.maskDir, "0001.png"), os.path.join(tool_gauss.maskDir, image_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Counts the number of black pixels in images contained in a folder
    It looks for the image with the highest number of black pixels and adds a new mask at that position. It repeats that process until a certain threshold is reached
    """)

    parser.add_argument("--threshold",
        help="The threshold when to stop in percent",
        type=float
    )

    args = parser.parse_args()
    loop(args.threshold)