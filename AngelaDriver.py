import maya.cmds as cmds
import json
Visemes_list = []
def add_some_vibrato():
    import maya.cmds as cmds
    import json

    def vibrato_decay(t):
        # t in (0, 1)


    starting_frame = 66
    ending_frame = 102
    fps = 24
    frequency = 5  # the lip will move 5 times per second
    vibrato_height = 0.1

    vibrato_dire = -1
    cmds.currentTime(starting_frame)
    cmds.select("angela_headMesh")
    current_frame = starting_frame
    step_size = int(fps / frequency)

    while current_frame <= ending_frame:
        cmds.currentTime(current_frame)
        if current_frame == starting_frame:
            cmds.select("CNT_JAW")
            cmds.move(0, vibrato_height * vibrato_dire * 2, 0, relative=True)
        else:
            cmds.select("CNT_JAW")
            cmds.move(0, vibrato_height * vibrato_dire, 0, relative=True)
        cmds.setKeyframe(
            "|JALI_GRP|jRig_GRP|masterGRP|FACSMaster|FACSMasterGRP|FACSMaster_ctls|FACS_universal_GRP|CNT_JAW_GRP|CNT_JAW.translate")
        current_frame = current_frame + step_size
        vibrato_dire = vibrato_dire * -1


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



