import json

input_file = 'E:/MASC/Structured_data/child_in_time/audio_jali_MVP.json'
# input_file = "C:/Users/evansamaa/Desktop/vowel_model_dataset/A_I_A_I_A_I.json"
with open(input_file) as f:
    data = json.load(f)
data = json.loads(data)
# inputs
VOWELS_JALI = set(
    ["Ih_pointer", "Ee_pointer", "Eh_pointer", "Aa_pointer", "U_pointer", "Uh_pointer", "Oo_pointer", "Oh_pointer",
     "Schwa_pointer", "Eu_pointer", "Ah_pointer"])
CONSONANTS_JALI = set(
    ["BP_pointer", "M_pointer", "JY_pointer", "Th_pointer", "ShChZh_pointer", "SZ_pointer", "GK_pointer",
     "LNTD_pointer", "R_pointer", "W_pointer", "FV_pointer"])
CONSONANTS_NOJAW_JALI = set(
    ["Ya_pointer", "Ja_pointer", "Ra_pointer", "FVa_pointer", "LNTDa_pointer", "Ma_pointer", "BPa_pointer",
     "Wa_pointer", "Tha_pointer", "GKa_pointer"])
JALI_SLIDERS_SET = set.union(VOWELS_JALI, CONSONANTS_JALI, CONSONANTS_NOJAW_JALI)

for item in list(JALI_SLIDERS_SET):
    cmds.cutKey(item, clear=True)
cmds.cutKey("JaliJoystick", clear=True)
cmds.cutKey("Dimple", clear=True)
cmds.cutKey("Pucker", clear=True)
viseme_lists = data["viseme"][0]
viseme_intervals = data["viseme"][1]
ja_pts = data["jaw"]
li_pts = data["lip"]

fps = 24
for i in range(0, len(viseme_lists)):
    viseme_slider = viseme_lists[i]
    attribute = "ty"
    for pt in viseme_intervals[i]:
        cmds.setKeyframe(viseme_slider, at=attribute, v=pt[1], t=pt[0] * fps)
# get the jaw parameters in
viseme_slider = "JaliJoystick"
attribute = "Jaw"
for i in range(0, len(ja_pts)):
    cmds.setKeyframe(viseme_slider, at=attribute, v=ja_pts[i][1], t=ja_pts[i][0] * fps)
attribute = "Lip"
for i in range(0, len(li_pts)):
    cmds.setKeyframe(viseme_slider, at=attribute, v=li_pts[i][1], t=li_pts[i][0] * fps)

# get some good jaw brato motion
try:
    vib_intervals = data["vib"]
    slider = "JaliJoystick"
    attribute = "Jaw"
    for i in range(0, len(vib_intervals)):
        starting_frame = vib_intervals[i][0] * fps
        ending_frame = vib_intervals[i][1] * fps
        vibrato_frequency = 14  # the lip will move 5 times per second
        vibrato_height = 0.1

        vibrato_dire = -1
        t = starting_frame
        step_size = int(fps / vibrato_frequency)
        offsets = []
        while t <= ending_frame:
            offset = cmds.getAttr(slider + '.' + attribute, t=t)
            offsets.append(offset)
            t = t + step_size
        t = starting_frame
        counter = 0
        while t <= ending_frame:
            cmds.setKeyframe(slider, at=attribute, v=offsets[counter] + vibrato_height * vibrato_dire, t=t)
            t = t + step_size
            vibrato_dire = vibrato_dire * -1
            counter = counter + 1
except:
    print("no vib data")

try:
    modification_sliders, modification_ctrl_pts = data["vowel_mod"]
    for i in range(0, len(modification_sliders)):
        cmds.setKeyframe(modification_sliders[i][0], at=modification_sliders[i][1], v=modification_ctrl_pts[i][1],
                         t=modification_ctrl_pts[i][0] * fps)
except:
    print("no vowel mod data")

