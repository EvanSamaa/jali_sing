import json

with open('E:/Structured_data/rolling_in_the_deep_adele/audio_animation_data.json') as f:
  data = json.load(f)
data = json.loads(data)
# inputs
eye_brow_animation_commands = data["brow"][0]
eye_brow_animation_intervals = data["brow"][1]
finer_eye_brow_raise_intervals = data["brow"][2]
finer_eye_brow_furrow_intervals = data["brow"][3]

blink_animation_commands = data["blink"][0]
blink_animation_intervals = data["blink"][1]
fps = 24
cmds.cutKey("blink", at="LidDown")
cmds.cutKey("faceSlider_symm_parent_L|BrowInDown_GRP|BrowInDown", at="BrowIn")
cmds.cutKey("BrowRaise", at="BrowRaise")
# for i in range(0, 0):
for i in range(0, len(eye_brow_animation_intervals)):
    command = eye_brow_animation_commands[i]
    interval = eye_brow_animation_intervals[i]
    if command == "furrow":
        slider = "faceSlider_symm_parent_L|BrowInDown_GRP|BrowInDown"
        attribute = "BrowIn"
        output_tangent_type = "auto"
    elif command == "raise":
        slider = "BrowRaise"
        attribute = "BrowRaise"
        output_tangent_type  = "auto"
    for pi in range(0, len(interval)):
        ott = output_tangent_type
        if pi == 0:
            ott = "linear"
        cmds.setKeyframe(slider, at=attribute, v = interval[pi][1], t = interval[pi][0] * fps, ott = ott)
for i in range(0, len(blink_animation_commands)):
    command = blink_animation_commands[i]
    interval = blink_animation_intervals[i]
    slider = "blink"
    attribute = "LidDown"
    for pi in interval:
        cmds.setKeyframe(slider, at=attribute, v = pi[1], t = pi[0] * fps)
offsets = []
slider = "BrowRaise"
attribute = "BrowRaise"
for i in range(0, len(finer_eye_brow_raise_intervals)):
    t = finer_eye_brow_raise_intervals[i][0]
    offset = cmds.getAttr(slider + '.' + attribute, t = t * fps)
    offsets.append(offset)
for i in range(0, len(finer_eye_brow_raise_intervals)):
    t = finer_eye_brow_raise_intervals[i][0]
    relative_value = finer_eye_brow_raise_intervals[i][1]
    cmds.setKeyframe(slider, at=attribute, v=offsets[i] + relative_value, t=t * fps)
