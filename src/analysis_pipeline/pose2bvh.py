import numpy as np
import math

joint_order = []

def joint2bvh(name, joint_offsets, joint_children):
    offset = joint_offsets[name]
    if len(joint_children[name]) == 0:
        return f"End Site\n{{\nOFFSET {round(offset[0],2)} {round(offset[1],2)} {round(offset[2],2)}\n}}\n"

    joint_order.append(name)
    if len(joint_children[name]) == 1 and len(joint_children[joint_children[name][0]]) == 0:
        child_offset = joint_offsets[joint_children[name][0]]
        body = f"End Site\n{{\nOFFSET {round(child_offset[0],2)} {round(child_offset[1],2)} {round(child_offset[2],2)}\n}}\n"
    else:
        body = children2bvh(name, joint_offsets, joint_children)
    bvh = f"JOINT {name}\n{{\nOFFSET {round(offset[0],2)} {round(offset[1],2)} {round(offset[2],2)}\nCHANNELS 3 Zrotation Xrotation Yrotation\n{body}}}"
    return bvh

def children2bvh(parent, joint_offsets, joint_children):
    bvh = ""
    children_number = len(joint_children[parent])
    if children_number > 1:
        for i in range(children_number):
            joint_order.append(f"{parent}{i}")
            bvh += f"JOINT {parent}{i}\n{{\nOFFSET 0.00 0.00 0.00\nCHANNELS 3 Zrotation Xrotation Yrotation\n{joint2bvh(joint_children[parent][i], joint_offsets, joint_children)}\n}}\n"
    elif children_number == 1:
        bvh += f"{joint2bvh(joint_children[parent][0], joint_offsets, joint_children)}\n"
    return bvh

def world2local(child_pos, parent_pos):
    return (np.array(child_pos) - np.array(parent_pos)).tolist()

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
        if p == j:
            continue
        joint_children[p].append(j)
    
    joint_offsets = {}
    for j in joint_names:
        joint_offsets[j] = world2local(joint_frames[j][0], joint_frames[joint_parents[j]][0])

    root_body = children2bvh("torso", joint_offsets, joint_children)
    frame_count = len(joint_frames["head"])
    bvh = f"HIERARCHY\nROOT torso\n{{\nOFFSET 0.00 0.00 0.00\nCHANNELS 3 Xposition Yposition Zposition\n{root_body}}}\nMOTION\nFrames: {frame_count}\nFrame Time: {1/fps}\n"

    for i in range(frame_count):
        torso_pos = joint_frames["torso"][i]
        bvh += f"{round(torso_pos[0],2)} {round(torso_pos[1],2)} {round(torso_pos[2],2)} "
        for j in joint_order:
            if j[-1].isdigit():
                parent = j[:-1]
                child = joint_children[parent][int(j[-1])]
            else:
                parent = j
                child = joint_children[parent][0]
            initial_pos = (np.array(joint_frames[parent][i]) + np.array(joint_offsets[child])).tolist()
            current_pos = joint_frames[child][i]

            initial_z_rot = math.degrees(math.atan2(initial_pos[1], initial_pos[0]))
            initial_x_rot = math.degrees(math.atan2(initial_pos[1], initial_pos[2]))
            initial_y_rot = math.degrees(math.atan2(initial_pos[0], initial_pos[2]))

            z_rot = math.degrees(math.atan2(current_pos[1], current_pos[0]))
            x_rot = math.degrees(math.atan2(current_pos[1], current_pos[2]))
            y_rot = math.degrees(math.atan2(current_pos[0], current_pos[2]))

            bvh += f"{round(z_rot-initial_z_rot,2)} {round(x_rot-initial_x_rot,2)} {round(y_rot-initial_y_rot,2)} "
        bvh += "\n"

    return bvh
