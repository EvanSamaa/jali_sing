import json

input_file = "F:\\MASC\\Jali_sing\\\Revision\\Lip Sync live performances\\april_houston\\jali_MVP.json"


# input_file = "F:/MASC/Jali_sing/Revision/validation/faceware session Indian Classical singer/pia dana/pia_jali_MVP.json"
# input_file = "F:\\MASC\\Jali_sing\\Revision\\Revision_submission_Video\\intro_sentence\\jali_MVP.json"
# input_file = "C:/Users/evansamaa/Desktop/vowel_model_dataset/A_I_A_I_A_I.json"
# input_file = "F:\\MASC\\Jali_sing\\Sig_videos\\song2face3\\song2face_3\\audio_jali_MVP.json"
# input_file = "F:\\MASC\\Jali_sing\\Sig_videos\\child_in_time\\audio_jali_MVP.json"

def init_blend_nodes():
    # test = cmds.createNode( 'pairBlend', n='Ih_pointer'+'_pairBlend_M_Vnot' )
    # Connect the translation of two nodes together
    # cmds.connectAttr( 'Pitch_Sensitivity.pitch_sensitivity', 'Ih_pointer'+'_pairBlend_M_Vnot.weight' )

    VOWELS_JALI = set(
        ["Ih_pointer", "Ee_pointer", "Eh_pointer", "Aa_pointer", "U_pointer", "Uh_pointer", "Oo_pointer", "Oh_pointer",
         "Schwa_pointer", "Eu_pointer", "Ah_pointer"])
    CONSONANTS_JALI = set(
        ["BP_pointer", "M_pointer", "JY_pointer", "Th_pointer", "ShChZh_pointer", "SZ_pointer", "GK_pointer",
         "LNTD_pointer", "R_pointer", "W_pointer", "FV_pointer"])
    CONSONANTS_NOJAW_JALI = set(
        ["Ya_pointer", "Ja_pointer", "Ra_pointer", "FVa_pointer", "LNTDa_pointer", "Ma_pointer", "BPa_pointer",
         "Wa_pointer", "Tha_pointer", "GKa_pointer"])
    JALI_JOYSTICK = set(["JaliJoystick_Lip", "JaliJoystick_Jaw"])

    JALI_SLIDERS_SET = set.union(VOWELS_JALI, CONSONANTS_JALI, CONSONANTS_NOJAW_JALI, JALI_JOYSTICK)

    for item in list(JALI_SLIDERS_SET):
        try:
            cmds.delete(item + '_pairBlend_M_Pnot')
            cmds.delete(item + '_pairBlend_M_P')
            cmds.delete(item + '_pairBlend_P')
        except:
            pass
        try:
            cmds.delete(item + '_Mnot_Pnot')
        except:
            pass
        try:
            cmds.delete(item + '_M_Pnot')
        except:
            pass
        try:
            cmds.delete(item + '_Mnot_P')
        except:
            pass
        try:
            cmds.delete(item + '_M_P')
        except:
            pass

        # this blends between two sets of musical articulation without pitch sensitivity
        cmds.createNode('pairBlend', n=item + '_pairBlend_M_Pnot')
        # this blends between two sets of musical articulation with pitch sensitivity
        cmds.createNode('pairBlend', n=item + '_pairBlend_M_P')
        # this blends between two sets of musical articulation with pitch sensitivity
        cmds.createNode('pairBlend', n=item + '_pairBlend_P')
        cmds.connectAttr('Musical_Articulation.musical_articulation', item + '_pairBlend_M_P.weight')
        cmds.connectAttr('Musical_Articulation.musical_articulation', item + '_pairBlend_M_Pnot.weight')
        cmds.connectAttr('Pitch_Sensitivity.pitch_sensitivity', item + '_pairBlend_P.weight')
        cmds.connectAttr(item + '_pairBlend_M_P.outTranslateX', item + '_pairBlend_P.inTranslateX2')
        cmds.connectAttr(item + '_pairBlend_M_Pnot.outTranslateX', item + '_pairBlend_P.inTranslateX1')
        if item != "JaliJoystick_Jaw" and item != "JaliJoystick_Lip":
            cmds.connectAttr(item + '_pairBlend_P.outTranslate.outTranslateX', item + '.translate.translateY')
        else:
            cmds.connectAttr(item + '_pairBlend_P.outTranslate.outTranslateX',
                             item.split("_")[0] + "." + item.split("_")[1], force=True)
        cmds.createNode('animCurveTL', n=item + '_M_P')
        cmds.createNode('animCurveTL', n=item + '_Mnot_P')
        cmds.createNode('animCurveTL', n=item + '_M_Pnot')
        cmds.createNode('animCurveTL', n=item + '_Mnot_Pnot')

        cmds.connectAttr(item + '_M_P.output', item + '_pairBlend_M_P.inTranslateX2')
        cmds.connectAttr(item + '_Mnot_P.output', item + '_pairBlend_M_P.inTranslateX1')
        cmds.connectAttr(item + '_M_Pnot.output', item + '_pairBlend_M_Pnot.inTranslateX2')
        cmds.connectAttr(item + '_Mnot_Pnot.output', item + '_pairBlend_M_Pnot.inTranslateX1')

    vowel_mod_sliders = [["Dimple", "Dimple"], ["Pucker", "Pucker"],
                         ["Ee_pointer", "lipCornerPull"], ["Ee_pointer", "lipStretch"],
                         ["Eh_pointer", "lipCornerPull"], ["Eh_pointer", "lipStretch"],
                         ["Oo_pointer", "lipPucker"], ["U_pointer", "lipPucker"]]
    for item in list(vowel_mod_sliders):
        try:
            cmds.delete(item[0] + "_" + item[1] + '_M')
        except:
            pass
        try:
            cmds.delete(item[0] + "_" + item[1] + '_Mnot')
        except:
            pass
        try:
            cmds.delete('pairBlend', n=item[0] + "_" + item[1] + '_pairBlend_M')
        except:
            pass
        cmds.createNode('pairBlend', n=item[0] + "_" + item[1] + '_pairBlend_M')
        cmds.connectAttr('Musical_Articulation.musical_articulation', item[0] + "_" + item[1] + '_pairBlend_M.weight')
        cmds.createNode('animCurveTL', n=item[0] + "_" + item[1] + '_M')
        cmds.createNode('animCurveTL', n=item[0] + "_" + item[1] + '_Mnot')
        cmds.connectAttr(item[0] + "_" + item[1] + '_M.output', item[0] + "_" + item[1] + '_pairBlend_M.inTranslateX2')
        cmds.connectAttr(item[0] + "_" + item[1] + '_Mnot.output',
                         item[0] + "_" + item[1] + '_pairBlend_M.inTranslateX1')
        cmds.connectAttr(item[0] + "_" + item[1] + '_pairBlend_M.outTranslate.outTranslateX', item[0] + "." + item[1])


def gen_mvp_curves(input_file):
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

    init_blend_nodes()

    cmds.cutKey("Viseme_Enunciation", clear=True)
    cmds.cutKey("JaliJoystick", clear=True)
    cmds.cutKey("CNT_LOFACE.Dimple", clear=True)
    cmds.cutKey("CNT_LOFACE.Pucker", clear=True)
    cmds.cutKey("CNT_HYOID", clear=True)
    viseme_lists_M_Pnot = data["M_Pnot_viseme"][0]
    viseme_intervals_M_Pnot = data["M_Pnot_viseme"][1]
    viseme_lists_M_P = data["M_P_viseme"][0]
    viseme_intervals_M_P = data["M_P_viseme"][1]
    viseme_lists_Mnot_P = data["Mnot_P_viseme"][0]
    viseme_intervals_Mnot_P = data["Mnot_P_viseme"][1]
    viseme_lists_Mnot_Pnot = data["Mnot_Pnot_viseme"][0]
    viseme_intervals_Mnot_Pnot = data["Mnot_Pnot_viseme"][1]
    ja_pts = data["jaw"]
    li_pts = data["lip"]
    fps = 24

    for i in range(0, len(viseme_lists_M_Pnot)):
        node = viseme_lists_M_Pnot[i] + "_M_Pnot"
        attribute = "ty"
        for pt in viseme_intervals_M_Pnot[i]:
            cmds.setKeyframe(node, v=pt[1], t=pt[0] * fps)
    for i in range(0, len(viseme_lists_M_Pnot)):
        node = viseme_lists_M_P[i] + "_M_P"
        attribute = "ty"
        for pt in viseme_intervals_M_P[i]:
            cmds.setKeyframe(node, v=pt[1], t=pt[0] * fps)
    for i in range(0, len(viseme_lists_M_Pnot)):
        node = viseme_lists_Mnot_P[i] + "_Mnot_P"
        attribute = "ty"
        for pt in viseme_intervals_Mnot_P[i]:
            cmds.setKeyframe(node, v=pt[1], t=pt[0] * fps)
    for i in range(0, len(viseme_lists_M_Pnot)):
        node = viseme_lists_Mnot_Pnot[i] + "_Mnot_Pnot"
        attribute = "ty"
        for pt in viseme_intervals_Mnot_Pnot[i]:
            cmds.setKeyframe(node, v=pt[1], t=pt[0] * fps)

        # get the jaw parameters in
    # viseme_slider = "Viseme_Enunciation"
    # attribute = "translateY"

    # for i in range(0, len(ja_pts)):
    #    cmds.setKeyframe(viseme_slider, at=attribute, v=(ja_pts[i][1]/2.542 + 147.410), t=ja_pts[i][0] * fps)
    slider = "JaliJoystick"
    attribute = "Jaw"
    for i in range(0, len(ja_pts)):
        cmds.setKeyframe(slider + "_Jaw_" + "M_P", v=(ja_pts[i][1]), t=ja_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Jaw_" + "Mnot_P", v=(ja_pts[i][1]), t=ja_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Jaw_" + "M_Pnot", v=(ja_pts[i][1]), t=ja_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Jaw_" + "Mnot_Pnot", v=(ja_pts[i][1]), t=ja_pts[i][0] * fps)
    slider = "JaliJoystick"
    attribute = "Lip"
    for i in range(0, len(li_pts)):
        cmds.setKeyframe(slider + "_Lip_" + "M_P", v=(ja_pts[i][1]), t=ja_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Lip_" + "Mnot_P", v=(ja_pts[i][1]), t=ja_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Lip_" + "M_Pnot", v=(ja_pts[i][1]), t=ja_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Lip_" + "Mnot_Pnot", v=(ja_pts[i][1]), t=ja_pts[i][0] * fps)
        # get that throat motions yet
    throat_movement = data["throat"]
    for i in range(0, len(throat_movement)):
        for k in range(0, len(throat_movement[i])):
            cmds.setKeyframe("CNT_HYOID", at="Hyoid_inOut", v=throat_movement[i][k][1],
                             t=throat_movement[i][k][0] * fps)
            cmds.setKeyframe("CNT_HYOID", at="Hyoid_downUp", v=throat_movement[i][k][1],
                             t=throat_movement[i][k][0] * fps)

    # get some good jaw brato motion
    if True:
        vib_intervals = data["vib"]
        # slider = "Viseme_Enunciation"
        # attribute = "translateY"

        slider = "JaliJoystick"
        attribute = "Jaw"
        for i in range(0, len(vib_intervals)):
            starting_frame = vib_intervals[i][0] * fps
            ending_frame = vib_intervals[i][1] * fps

            vibrato_frequency = 10  # the lip will move 5 times per second
            vibrato_height_initial = 0
            vibrato_height_final = 0.6

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
                vibrato_height = vibrato_height_initial + (vibrato_height_final - vibrato_height_initial) * (
                        t - starting_frame) / (ending_frame - starting_frame)
                cmds.setKeyframe(slider + "_Jaw_" + "M_P", v=offsets[counter] + vibrato_height * vibrato_dire, t=t)
                cmds.setKeyframe(slider + "_Jaw_" + "Mnot_P", v=offsets[counter] + vibrato_height * vibrato_dire, t=t)
                t = t + step_size
                vibrato_dire = vibrato_dire * -1
                counter = counter + 1
            cmds.setKeyframe(slider + "_Jaw_" + "M_P", v=offsets[0], t=t)
            cmds.setKeyframe(slider + "_Jaw_" + "Mnot_P", v=offsets[0], t=t)

    modification_sliders, modification_ctrl_pts = data["vowel_mod_M"]
    for i in range(0, len(modification_sliders)):
        for j in range(0, len(modification_ctrl_pts[i])):
            cmds.setKeyframe(modification_sliders[i][0] + "_" + modification_sliders[i][1] + "_M",
                             v=modification_ctrl_pts[i][j][1],
                             t=modification_ctrl_pts[i][j][0] * fps)
    modification_sliders, modification_ctrl_pts = data["vowel_mod_M_not"]
    for i in range(0, len(modification_sliders)):
        for j in range(0, len(modification_ctrl_pts[i])):
            cmds.setKeyframe(modification_sliders[i][0] + "_" + modification_sliders[i][1] + "_Mnot",
                             v=modification_ctrl_pts[i][j][1],
                             t=modification_ctrl_pts[i][j][0] * fps)
    print("completed " + input_file)


gen_mvp_curves(input_file)
