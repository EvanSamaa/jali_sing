import json

landmark_data = "C:\Users\evansamaa\Desktop\lmbmm_VocalSep\jaliVertex2Landmark_dict.json"
with open(landmark_data) as f:
    V2L = json.load(f)
landmark_sets = ["nose", "lips", "lower_face"]
cmds.select(clear=True)
for lm_set in landmark_sets:
    marks = V2L[lm_set]
    for mark in marks.keys():
        cmds.select("head_lorez.vtx[{}]".format(mark), add=True)
