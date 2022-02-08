import numpy as np
import cv2
from os import listdir, mkdir
from os.path import isfile, isdir, join


def skeleton_to_image(img_path, out_path):
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

    image = np.array(image)
    image /= np.abs(image).max()    # normalise to [-1,1]
    cv2.imwrite(out_path, (image+1)*127.5)  # fit image data to [0,255]
    

def process_skeletons(root, out_dir):
    if not isdir(out_dir):
        mkdir(out_dir)
    
    skeleton_paths = [f for f in listdir(root) if isfile(join(root, f))]
    for s in skeleton_paths:
        skeleton_to_image(root + s, out_dir + s[:-4] + ".png")

if __name__ == "__main__":
    amateur_root = "data/THETIS_Skeletal_Joints/normal_oniFiles/ONI_AMATEURS/"
    shot_paths = [d for d in listdir(amateur_root) if isdir(join(amateur_root, d))]
    for s in shot_paths:
        process_skeletons(amateur_root + s + "/", "data/skeleton_images/amateur_" + s + "/")

    expert_root = "data/THETIS_Skeletal_Joints/normal_oniFiles/ONI_EXPERTS/"
    shot_paths = [d for d in listdir(expert_root) if isdir(join(expert_root, d))]
    for s in shot_paths:
        process_skeletons(expert_root + s + "/", "data/skeleton_images/expert_" + s + "/")

