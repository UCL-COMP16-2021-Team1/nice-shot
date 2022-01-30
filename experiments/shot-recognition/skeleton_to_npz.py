#  Written on the 30th of January 2022 by Morgane Ohlig
#  This converts the skeleton .txt input data from the Thetis dataset to .npz files for data to then be collected. Excludes fuzzied data.
from os import listdir, mkdir
import os
from os import path
import numpy as np

EXPERTISE_LEVELS = ['ONI_AMATEURS', 'ONI_EXPERTS']


def create_output_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.mkdir(path)


def skeleton_to_matrix(data_path:str) -> list:
    joint_no: int = 0
    matrices = tuple([[] for _ in range(15)])
    with open(data_path) as file:
        for line in file:
            if '\n' == line: # end of file
                break
            if 'FRAME' in line: # start filling in data for next frame
                joint_no = 0
                continue
            coordinates = [float(c) for c in line.split(' ')]
            matrices[joint_no].append(coordinates) # adds the coordinates for one frame
            joint_no += 1
    return np.asarray(matrices)


def download_shot_data(in_dir: str, out_dir: str, shot_file_name: str) -> None:
    filename: str = path.join(out_dir, f'graph_{shot_file_name}')
    matrix_array: list = skeleton_to_matrix(in_dir)
    np.savez(
        filename, 
        HEAD = matrix_array[0], 
        LEFT_ELBOW = matrix_array[1], 
        LEFT_FOOT = matrix_array[2], 
        LEFT_HAND = matrix_array[3], 
        LEFT_HIP = matrix_array[4], 
        LEFT_KNEE = matrix_array[5], 
        LEFT_SHOULDER = matrix_array[6], 
        NECK = matrix_array[7], 
        RIGHT_ELBOW = matrix_array[8], 
        RIGHT_FOOT = matrix_array[9], 
        RIGHT_HAND = matrix_array[10], 
        RIGHT_HIP = matrix_array[11],
        RIGHT_KNEE = matrix_array[12], 
        RIGHT_SHOULDER = matrix_array[13], 
        TORSO = matrix_array[14]
    ) # would like to avoid hardcoding this


def read_shot_contents(in_dir: str, out_dir: str) -> None:
    create_output_dir(out_dir)
    for shot_file in [ _ for _ in listdir(in_dir)]:
        download_shot_data(
            path.join(in_dir, shot_file),
            out_dir,
            shot_file.replace('.txt', '')
            )


def read_expertise_contents(in_dir: str, out_dir: str) -> None:
    create_output_dir(out_dir)
    for shot in [_ for _ in listdir(in_dir) if path.isdir(path.join(in_dir, _))]:
        read_shot_contents(
            path.join(in_dir, shot),
            path.join(out_dir, shot)
        )


if __name__ == '__main__':
    out_dir: str = './data/skeleton_npz'
    create_output_dir(out_dir)
    for expertise_lvl in EXPERTISE_LEVELS:
        read_expertise_contents(
            path.join('./data/THETIS_Skeletal_Joints/normal_oniFiles/', expertise_lvl),
            path.join(out_dir, expertise_lvl)
        )
