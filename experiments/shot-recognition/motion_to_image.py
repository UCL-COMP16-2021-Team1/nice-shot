import numpy as np
import cv2
from os import listdir, mkdir
from os.path import isfile, isdir, join


def motion_to_image(img_path, out_path):
    image = []

    with open(img_path) as file:
        for line in file:
            if line == "\n":
                break

            if "FRAME" in line:
                image.append([])
                continue

            coords = [float(c) for c in line.split(" ")]
            image[-1].append(coords)

    motion_image = image.copy()
    for t in range(len(image)-1):
        for n in range(len(image[t])):
            motion_image[t][n][0] = image[t+1][n][0] - image[t][n][0]
            motion_image[t][n][1] = image[t+1][n][1] - image[t][n][1]
            motion_image[t][n][2] = image[t+1][n][2] - image[t][n][2]
    motion_image.pop()

    motion_image = np.array(motion_image)
    motion_image /= np.abs(motion_image).max()    # normalise to [-1,1]
    cv2.imwrite(out_path, (motion_image+1)*127.5)  # fit image data to [0,255]
    

def process_motions(root, out_dir, _type):
    if not isdir(out_dir):
        mkdir(out_dir)
    
    skeleton_paths = [f for f in listdir(root) if isfile(join(root, f))]
    for s in skeleton_paths:
        motion_to_image(root + s, out_dir + _type + "_" + s[:-4] + ".png")

if __name__ == "__main__":
    amateur_root = "data/THETIS_Skeletal_Joints/normal_oniFiles/ONI_AMATEURS/"
    shot_paths = [d for d in listdir(amateur_root) if isdir(join(amateur_root, d))]
    for s in shot_paths:
        process_motions(amateur_root + s + "/", "data/motion_images/" + s + "/", "amateur")

    expert_root = "data/THETIS_Skeletal_Joints/normal_oniFiles/ONI_EXPERTS/"
    shot_paths = [d for d in listdir(expert_root) if isdir(join(expert_root, d))]
    for s in shot_paths:
        process_motions(expert_root + s + "/", "data/motion_images/" + s + "/", "expert")