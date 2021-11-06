import cv2
import argparse
import os
import os.path as path
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp

import config

cores = mp.cpu_count()


def count_pixels(image_path):
    # Count the number of black pixels in an image provided an image path
    image = cv2.imread(image_path, 0)
    num_black = image.size - cv2.countNonZero(image)
    return num_black / image.size

def get_image_paths(folder_path):
    # Get image paths
    image_names = [f for f in os.listdir(folder_path) if path.isfile(path.join(folder_path, f))]
    image_names.sort()
    image_paths = [path.join(folder_path, f) for f in image_names]
    image_paths = image_paths[int(config.frameFirst) - 1: int(config.frameLast) + 1]
    return image_paths

def count_pixels_masked(image_path):
    mask_path = path.join(config.maskDir, path.basename(image_path))

    # Read image and mask
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Mask image
    image = cv2.bitwise_and(image, image, mask=mask)

    # Count nonZero
    num_black = image.size - cv2.countNonZero(image)
    return num_black / image.size

def go_through_images(folder_path, pixel_adjust=False):
    image_paths = get_image_paths(folder_path)
    image_names = [path.basename(p) for p in image_paths]

    # Count black pixels in images
    pool = mp.Pool(cores)

    # Individually adjust pixel sizes
    if pixel_adjust:
        #num_blacks = pool.map(count_pixels_masked, image_paths)
        num_blacks = list(map(count_pixels_masked, image_paths))
        num_blacks = np.array(num_blacks) - np.array(pixel_adjust)
        num_blacks = [max(0, b) for b in num_blacks]
    # Don't adjust is equivalent to full mask
    else:
        num_blacks = pool.map(count_pixels, image_paths)

    # Get statistics
    max_black = np.argmax(num_blacks)
    print("The image with the most black pixels: " +image_names[max_black])
    print(f"Percentage of maximum number of pixels: {num_blacks[max_black]*100:.1f}")

    # Output statistics
    plt.plot(num_blacks, label="before " + image_names[max_black])
    plt.legend()
    plt.savefig("num_black.png")
    return image_names[max_black], num_blacks[max_black]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Counts the number of black pixels in images contained in a folder
    It prints the image with the most black pixels (add gaussian mask)
    and also creates a graph with the distribution of black pixels""")

    parser.add_argument("--folder-path", 
        help="The path to the folder with the gauss images",
        required=True)

    args = parser.parse_args()
    go_through_images(args.folder_path)

