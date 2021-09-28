import maya.cmds as cmds
import json
Visemes_list = []

def read_neck_movement_json(file_name):
    neck_movement_dict = json.load(file_name)

def set_current_time(t):
    cmds.currentTime(t)

import maya.cmds as cmds
import json


read_neck_movement_json()
max_frames = 330
cmds.playbackOptions(min=0, max=max_frames)
cmds.currenttime(0)
cmds.select("angela_headMesh")
cmds.select("jNeck_ctl")
cmds.rotate(0, 0, 0, relative = True, objectSpace = True, )



