from os import path

data_folder = "/home/martin/Videos/ondrej_et_al/bf/"
inputFileFormat = "%04d"    # name of input files, e.g., %03d if files are named 001.png, 002.png
generation_folder = "video"

inputPNG = inputFileFormat + ".png"

maskDir = path.join(data_folder, generation_folder, "mask")        # mask dir, essentially leading frames from where the gaussians will be propagated
maskFiles = path.join(maskDir,  inputFileFormat + ".png")


flowFwdDir = path.join(data_folder, generation_folder, "flow_fwd")
flowBwdDir = path.join(data_folder, generation_folder, "flow_bwd")
flowFwdFiles = path.join(flowFwdDir, inputFileFormat + ".A2V2f")  # path to the forward flow files (computed by _tools/disflow)
flowBwdFiles = path.join(flowBwdDir, inputFileFormat + ".A2V2f")  # path to the backward flow files (computed by _tools/disflow)

frameFirst = "0001"                  # name of the first PNG file in the input folder (without extension)
frameLast = "0400"                   # number of the last PNG file in the input folder (without extension)
frameStep = +1

gdisko_gauss_r10_s10_dir = path.join(data_folder,generation_folder, "input_gdisko_gauss_r10_s10")    # path to the result gauss r10 s10 sequence
gdisko_gauss_r10_s15_dir = path.join(data_folder,generation_folder, "input_gdisko_gauss_r10_s15")    # path to the result gauss r10 s15 sequence
gdisko_gauss_r10_s10_files = path.join(gdisko_gauss_r10_s10_dir, inputPNG)
gdisko_gauss_r10_s15_files = path.join(gdisko_gauss_r10_s15_dir, inputPNG) 

imageFormat   = path.join(data_folder, generation_folder, "input_filtered/", inputPNG)
outputFormat  = path.join(data_folder, generation_folder, "input_filtered/", inputPNG)  # path to the result filtered sequence

tools_path = "Few-Shot-Patch-Based-Training/_tools/"

bilateralExecutable = path.join(tools_path, "bilateralAdv/bilateralAdv")
disflowExecutable = path.join(tools_path, "disflow/disflow")
gaussExecutable = path.join(tools_path, "gauss/gauss")
