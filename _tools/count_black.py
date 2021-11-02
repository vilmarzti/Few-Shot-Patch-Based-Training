import cv2
import argparse
import os
import os.path as path
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp

cores = mp.cpu_count()


def count_pixels(image_path):
    # Count the number of black pixels in an image provided an image path
    image = cv2.imread(image_path, 0)
    num_black = image.size - cv2.countNonZero(image)
    return num_black


def go_through_images(folder_path):
    # Get image paths
    image_names = [f for f in os.listdir(folder_path) if path.isfile(path.join(folder_path, f))]
    image_names.sort()
    image_paths = [path.join(folder_path, f) for f in image_names]

    # Count black pixels in images
    pool = mp.Pool(cores)
    num_blacks = pool.map(count_pixels, image_paths)

    # Get statistics
    max_black = np.argmax(num_blacks)
    print(image_names[max_black])

    # Output statistics
    plt.plot(num_blacks)
    plt.savefig("num_black.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Counts the number of black pixels in images contained in a folder
    It prints the image with the most black pixels (add gaussian mask)
    and also creates a graph with the distribution of black pixels""")

    parser.add_argument("--folder-path", 
        help="The path to the folder with the gauss images",
        required=True)

    args = parser.parse_args()
    go_through_images(args.folder_path)

