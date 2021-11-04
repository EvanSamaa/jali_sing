import json
with open('E:/Structured_data/rolling_in_the_deep_adele/audio_animation_data.json') as f:
    data = json.load(f)
data = json.loads(data)
# inputs
VOWELS_JALI = set(["Ih_pointer", "Ee_pointer", "Eh_pointer", "Aa_pointer", "U_pointer", "Uh_pointer", "Oo_pointer", "Oh_pointer", "Schwa_pointer", "Eu_pointer", "Ah_pointer"])
CONSONANTS_JALI = set(["MBP_pointer", "JY_pointer", "Th_pointer", "ShChZh_pointer", "SZ_pointer", "GK_pointer", "LNTD_pointer", "R_pointer", "W_pointer", "FV_pointer"])
CONSONANTS_NOJAW_JALI = set(["Ya_pointer", "Ja_pointer", "Ra_pointer", "FVa_pointer", "LNTDa_pointer", "MBPa_pointer", "Wa_pointer", "Tha_pointer", "GKa_pointer"])
JALI_SLIDERS_SET = set.union(VOWELS_JALI, CONSONANTS_JALI, CONSONANTS_NOJAW_JALI)

for item in list(JALI_SLIDERS_SET):
    cmds.cutKey(item, clear=True)
viseme_lists = data["visemes"][0]
viseme_intervals = data["visemes"][1]
fps=24
for i in range(0, len(viseme_lists)):
    viseme_slider = viseme_lists[i]
    attribute = "ty"
    for pt in viseme_intervals[i]:
        cmds.setKeyframe(viseme_slider, at=attribute, v=pt[1], t=pt[0] * fps)
