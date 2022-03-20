import numpy as np
import copy
import math

def joint2bvh(name, joint_offsets, joint_children):
    offset = joint_offsets[name][0]
    if len(joint_children[name]) == 0:
        body = "End Site\n{\nOFFSET 0.00 0.00 0.00\n}\n"
    else:
        body = children2bvh(name, joint_offsets, joint_children)
    bvh = f"JOINT {name}\n{{\nOFFSET {round(offset[0],2)} {round(offset[1],2)} {round(offset[2],2)}\nCHANNELS 3 Zrotation Xrotation Yrotation\n{body}}}"
    return bvh

def children2bvh(parent, joint_offsets, joint_children):
    bvh = ""
    for j in joint_children[parent]:
        bvh += joint2bvh(j, joint_offsets, joint_children) + "\n"
    return bvh

def world2local(child_frames, parent_frames):
    return (np.array(child_frames) - np.array(parent_frames)).tolist()

def pose2bvh(joint_frames, fps):
    joint_parents = {
        "head": "neck",
        "left_elbow": "left_shoulder",
        "left_foot": "left_knee",
        "left_wrist": "left_elbow",
        "left_hip": "torso",
        "left_knee": "left_hip",
        "left_shoulder": "neck",
        "neck": "torso",
        "right_elbow": "right_shoulder",
        "right_foot": "right_knee",
        "right_wrist": "right_elbow",
        "right_hip": "torso",
        "right_knee": "right_hip",
        "right_shoulder": "neck",
        "torso": "torso"
    }

    joint_children = {
        "head": [],
        "left_elbow": [],
        "left_foot": [],
        "left_wrist": [],
        "left_hip": [],
        "left_knee": [],
        "left_shoulder": [],
        "neck": [],
        "right_elbow": [],
        "right_foot": [],
        "right_wrist": [],
        "right_hip": [],
        "right_knee": [],
        "right_shoulder": [],
        "torso": []
    }
    joint_names = joint_parents.keys()
    for j in joint_names:
        p = joint_parents[j]
        joint_children[p].append(j)
    joint_children["torso"].remove("torso")
    
    joint_offsets = copy.deepcopy(joint_frames)
    for j in joint_names:
        joint_offsets[j] = world2local(joint_frames[j], joint_frames[joint_parents[j]])

    root_body = children2bvh("torso", joint_offsets, joint_children)
    frame_count = len(joint_offsets["head"])
    bvh = f"HIERARCHY\nROOT torso\n{{\nOFFSET 0.00 0.00 0.00\nCHANNELS 3 Xposition Yposition Zposition\n{root_body}}}\nMOTION\nFrames: {frame_count}\nFrame Time: {1/fps}\n"

    motion_order = ["torso", "left_hip", "left_knee", "left_foot", "neck", "head", "left_shoulder", "left_elbow", "left_wrist", "right_shoulder", "right_elbow", "right_wrist", "right_hip", "right_knee", "right_foot"]
    for i in range(frame_count):
        for j in motion_order:
            offset = joint_offsets[j][i]
            bvh += f"{round(math.degrees(math.atan2(offset[0],offset[1])),2)} {round(math.degrees(math.atan2(offset[2],offset[1])),2)} {round(math.degrees(math.atan2(offset[0],offset[2])),2)} "
        bvh += "\n"

    f = open("test.bvh", "w")
    f.write(bvh)
    f.close()
