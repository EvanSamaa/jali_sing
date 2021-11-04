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
import json

with open('E:/Structured_data/rolling_in_the_deep_adele/audioanimation_data.json') as f:
    data = json.load(f)
data = json.loads(data)
# inputs
eye_brow_animation_commands = data["brow"][0]
eye_brow_animation_intervals = data["brow"][1]
fps = 24
onset = 0.2
offset = 0.2
eye_brow_animation_intervals = [[f[0] * fps, f[1] * fps] for f in eye_brow_animation_intervals]
print(eye_brow_animation_intervals)
for i in range(0, len(eye_brow_animation_intervals)):
    command = eye_brow_animation_commands[i]
    interval = eye_brow_animation_intervals[i]
    if command == "furrow":
        # set a zero before and after the curve starts
        cmds.currentTime(interval[0] - onset * fps)
        cmds.select("angela_headMesh")
        cmds.select("faceSlider_symm_parent_L|BrowInDown_GRP|BrowInDown")
        cmds.setAttr("BrowInDown.BrowIn", 0)
        cmds.setKeyframe(at="BrowIn")

        cmds.currentTime(interval[1] + offset * fps)
        cmds.select("faceSlider_symm_parent_L|BrowInDown_GRP|BrowInDown")
        cmds.setAttr("BrowInDown.BrowIn", 0)
        cmds.setKeyframe(at="BrowIn")

        # set values for the curve
        cmds.currentTime(interval[0])
        cmds.select("faceSlider_symm_parent_L|BrowInDown_GRP|BrowInDown")
        cmds.setAttr("BrowInDown.BrowIn", 10)
        cmds.setKeyframe(at="BrowIn")

        cmds.currentTime(interval[1])
        cmds.select("faceSlider_symm_parent_L|BrowInDown_GRP|BrowInDown")
        cmds.setAttr("BrowInDown.BrowIn", 10)
        cmds.setKeyframe(at="BrowIn")
    elif command == "raise":
        cmds.currentTime(interval[0] - onset * fps)
        cmds.select("angela_headMesh")
        cmds.select("BrowRaise")
        cmds.setAttr("BrowRaise.BrowRaise", 0)
        cmds.setKeyframe(at="BrowRaise")

        cmds.currentTime(interval[1] + offset * fps)
        cmds.select("BrowRaise")
        cmds.setAttr("BrowRaise.BrowRaise", 0)
        cmds.setKeyframe(at="BrowRaise")

        # set values for the curve
        cmds.currentTime(interval[0])
        cmds.select("BrowRaise")
        cmds.setAttr("BrowRaise.BrowRaise", 5)
        cmds.setKeyframe(at="BrowRaise")

        cmds.currentTime(interval[1])
        cmds.select("BrowRaise")
        cmds.setAttr("BrowRaise.BrowRaise", 5)
        cmds.setKeyframe(at="BrowRaise")
