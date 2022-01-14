'''
for processing all of the data and inserting it into graph files.
should make it into a graph and then store that in another file? or perhaps it'd be wiser to use this in the other ipynb file
since then I wouldn't have to store anything
or do I want to write it to a file?... I don't think that's a good idea, it'd make things more complicated than anything.
'''


import numpy

'''
pseudocode: 
when I read through the file each frame there are 15 joints.
For each joint I have to "read differently" I think?
so essentially:
AS I GO THROUGH THE FILE:
EACH TIME THERE'S A FRAME:
I HAVE TO RESTART THE PROCESS FOR EACH JOINT
so maybe I need to do this for each joint obj.
each frame is a file right? 
wait no
A WHOLE FILE = ONE .NPZ FILE
so basically I'd have to update the matrix as I go through the process
And once that's done I can do the whole spektral graph thing.

and this code is specifically for this matrix update thing
'''

joints = [
    'HEAD',
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
    'TORSO'
        ]

def skeleton_to_graph(data_path:str) -> list:  # return a more specific type. this is too vague
    # return array object in numpy
    # also need a frame counter
    frame_counter = -1
    joint_counter = 0
    matrices = tuple([[] for _ in range(15)])
    print(matrices)
    matrices[0].append("ass")
    print(matrices)
    with open(data_path) as file:
        print(matrices)
        # need to create a matrix thing too
        # one matrix for each joint
        for line in file:
            if '\n' == line: # end of file essentially
                break

            if 'FRAME' in line:
                # redo process or at least do it all again.
                # or maybe reset a joint counter. pretty primitive but it'll do for now OR I have a list of the joints that are mentioned and I can index to them with a list of the joints
                joint_counter = 0
                frame_counter +=1 # should be done after
                #print(f'FRAME COUNTER ({frame_counter} VS ACTUAL FRAME LINE ({line}))')
                # does the frame counter even matter here
                continue

            coordinates = [float(c) for c in line.split(' ')]
            # can I give names to the joints or
            #print(joint_counter)
            matrices[joint_counter].append(coordinates) # adds the coordinates for one frame
            #print(matrices)
            joint_counter += 1

      
    for matrix in matrices:
        print(f"KLJLHKGJT {matrix}")
        print(f"FINAL FRAME COUNT: {frame_counter}")
        print(f"MATRIX FRAME COUNT: {len(matrix)-1}")
        print("\n\n")
     
    
    return matrices

    

if __name__ == '__main__':

    skeleton_to_graph('data/THETIS_Skeletal_Joints/normal_oniFiles/ONI_AMATEURS/backhand/p1.txt')
    pass
