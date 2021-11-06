import os

################ MAKE CHANGES HERE #################
data_folder = "/home/martin/Documents/code/python/Few-Shot-Patch-Based-Training/TEST_DATA/"
inputFileFormat = "%04d"    # name of input files, e.g., %03d if files are named 001.png, 002.png
maskDir = data_folder + "/bf_train/mask_gauss_10"            # mask dir, essentially leading frames from where the gaussians will be propagated
maskFiles = maskDir + "/" + inputFileFormat + ".png"
flowFwdFiles = data_folder + "/bf_gen/flow_fwd" + "/" + inputFileFormat + ".A2V2f"  # path to the forward flow files (computed by _tools/disflow)
flowBwdFiles = data_folder +"/bf_gen/flow_bwd" + "/" + inputFileFormat + ".A2V2f"  # path to the backward flow files (computed by _tools/disflow)
frameFirst = "0001"                  # name of the first PNG file in the input folder (without extension)
frameLast = "0450"                   # number of the last PNG file in the input folder (without extension)
gdisko_gauss_r10_s10_dir = data_folder + "bf_gen/input_gdisko_gauss_r10_s10"    # path to the result gauss r10 s10 sequence
gdisko_gauss_r10_s15_dir = data_folder + "bf_gen/input_gdisko_gauss_r10_s15"    # path to the result gauss r10 s15 sequence
gdisko_gauss_r10_s10_files = gdisko_gauss_r10_s10_dir + "/" + inputFileFormat + ".png" 
gdisko_gauss_r10_s15_files = gdisko_gauss_r10_s15_dir + "/" + inputFileFormat + ".png" 
####################################################

def create_commands():
    if not os.path.exists(gdisko_gauss_r10_s10_dir):
        os.mkdir(gdisko_gauss_r10_s10_dir)
        
    if not os.path.exists(gdisko_gauss_r10_s15_dir):
        os.mkdir(gdisko_gauss_r10_s15_dir)

    masks_str = ""
    masks_list_dir = os.listdir(maskDir)
    for mask in masks_list_dir:
        masks_str += mask.replace(".png", "").replace(".jpg", "")
        masks_str += " "

    commands = [
        f"./gauss/gauss {maskFiles} {flowFwdFiles} {flowBwdFiles} {frameFirst} {frameLast} {len(masks_list_dir)} {masks_str} 10 10 {gdisko_gauss_r10_s10_files}",
        f"./gauss/gauss {maskFiles} {flowFwdFiles} {flowBwdFiles} {frameFirst} {frameLast} {len(masks_list_dir)} {masks_str} 10 15 {gdisko_gauss_r10_s15_files}"
    ]
    return commands

if __name__ == "__main__":
    commands = create_commands()
    os.system(commands[0])
    os.system(commands[1])
