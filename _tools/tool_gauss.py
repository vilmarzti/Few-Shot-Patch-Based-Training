import os
import config

def create_commands():
    if not os.path.exists(config.gdisko_gauss_r10_s10_dir):
        os.mkdir(config.gdisko_gauss_r10_s10_dir)
        
    if not os.path.exists(config.gdisko_gauss_r10_s15_dir):
        os.mkdir(config.gdisko_gauss_r10_s15_dir)

    masks_str = ""
    masks_list_dir = os.listdir(config.maskDir)
    for mask in masks_list_dir:
        masks_str += mask.replace(".png", "").replace(".jpg", "")
        masks_str += " "

    commands = [
        f"./gauss/gauss {config.maskFiles} {config.flowFwdFiles} {config.flowBwdFiles} {config.frameFirst} {config.frameLast} {len(masks_list_dir)} {masks_str} 10 10 {config.gdisko_gauss_r10_s10_files}",
        f"./gauss/gauss {config.maskFiles} {config.flowFwdFiles} {config.flowBwdFiles} {config.frameFirst} {config.frameLast} {len(masks_list_dir)} {masks_str} 10 15 {config.gdisko_gauss_r10_s15_files}"
    ]
    return commands

if __name__ == "__main__":
    commands = create_commands()
    os.system(commands[0])
    os.system(commands[1])
