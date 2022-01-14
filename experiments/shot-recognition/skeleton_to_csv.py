import csv
from os import listdir, mkdir
from os.path import isdir, join
from numpy import asarray, savetxt, ndarray
import os

joint_names = ['HEAD',
    'LEFT_ELBOW',
    'LEFT_FOOT',
    'LEFT_HAND',
    'LEFT_HIP',
    'LEFT_KNEE',
    'LEFT_SHOULDER',
    'NECK',
    'RIGHT_ELBOW',
    'RIGHT_FOOT',
    'RIGHT_HAND',
    'RIGHT_HIP',
    'RIGHT_KNEE',
    'RIGHT_SHOULDER',
    'TORSO']

def skeleton_to_matrix(data_path:str) -> list:  # return a more specific type. this is too vague
    joint_no = 0
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

    return asarray(matrices)


def process_shot_type(root:str, out_dir:str) -> None:
    create_dir(out_dir)
    skeleton_paths = [ _ for _ in listdir(root)]
    
    for s in skeleton_paths:
        csv_path = join(root, s)
        out_dir_csv = join (out_dir, s.replace('.txt',''))

        create_dir(out_dir_csv)
        
        matrix_array = skeleton_to_matrix(csv_path)

        joint_count = 0
        for joint in matrix_array:
           savetxt(join(out_dir_csv, joint_names[joint_count]) + '.csv', joint, delimiter=',')
           joint_count +=1


def process_via_expertise(root:str) -> None:
    shot_paths = [dir for dir in listdir(root) if isdir(join(root, dir))]
    for s in shot_paths:
        process_shot_type(join(root, s), 'data/skeleton_csv/' + s + "/")

def create_dir(dir):
    if not isdir(dir):
        mkdir(dir)

if __name__ == '__main__':

    create_dir('data/skeleton_csv')
    
    process_via_expertise('data/THETIS_Skeletal_Joints/normal_oniFiles/ONI_AMATEURS')
    process_via_expertise('data/THETIS_Skeletal_Joints/normal_oniFiles/ONI_EXPERTS')
