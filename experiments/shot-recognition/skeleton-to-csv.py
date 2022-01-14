from os import listdir
from os.path import isdir

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

    return matrices

if __name__ == '__main__':
    amateur_root = 'data/THETIS_Skeletal_Joints/normal_oniFiles/ONI_AMATEURS'
    shot_paths = [dir for dir in listdir(amateur_root) if isdir(amateur_root) and dir != '.DS_Store']

    for s in shot_paths:
        print(s)
        skeleton_paths = [f for f in listdir(amateur_root + '/' + s) if isdir(amateur_root + '/' + s)]
        skeleton_to_matrix(s)
        print(skeleton_paths)
