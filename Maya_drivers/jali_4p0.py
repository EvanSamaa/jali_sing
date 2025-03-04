import json
import maya.cmds as cmds

input_file = 'C:/Users/evan1/Desktop/music_companion/die_with_a_smile.json'

# Helper function for FACS sliders (blend mode)
def connect_with_blend(target_attr, new_source, blend_name, blend_weight=0.5):
    """If target_attr already has an incoming connection, blend it with new_source.
       Otherwise, connect new_source directly.
    """
    existing = cmds.listConnections(target_attr, s=True, d=False, plugs=True)
    if existing:
        # Grab first connection (assumes only one exists)
        ex_conn = existing[0]
        cmds.disconnectAttr(ex_conn, target_attr)
        # Create a new pairBlend node to mix the two inputs
        blend_node = cmds.createNode('pairBlend', n=blend_name)
        # For this example, we use the "inTranslateX" attribute – adjust if needed.
        cmds.connectAttr(ex_conn, blend_node + '.inTranslateX1')
        cmds.connectAttr(new_source, blend_node + '.inTranslateX2')
        cmds.setAttr(blend_node + '.weight', blend_weight)
        cmds.connectAttr(blend_node + '.outTranslateX', target_attr, force=True)
    else:
        cmds.connectAttr(new_source, target_attr)

# Helper function for viseme sliders (replace mode)
def replace_existing_connection(target_attr):
    """Disconnect any incoming connections from target_attr and delete the source node(s)."""
    existing = cmds.listConnections(target_attr, s=True, d=False, plugs=True)
    if existing:
        for conn in existing:
            cmds.disconnectAttr(conn, target_attr)
            # Delete the source node if safe (be cautious!)
            source_node = conn.split('.')[0]
            if cmds.objExists(source_node):
                cmds.delete(source_node)

def init_blend_nodes():
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

    # Process FACS sliders
    for item in list(JALI_SLIDERS_SET):
        # Try to delete any preexisting nodes created by our script
        for suffix in ['_pairBlend_M_Pnot', '_pairBlend_M_P', '_pairBlend_P',
                       '_Mnot_Pnot', '_M_Pnot', '_Mnot_P', '_M_P']:
            try:
                cmds.delete(item + suffix)
            except:
                pass

        # Create our pairBlend nodes and animCurves (this part is your original code)
        cmds.createNode('pairBlend', n=item + '_pairBlend_M_Pnot')
        cmds.createNode('pairBlend', n=item + '_pairBlend_M_P')
        cmds.createNode('pairBlend', n=item + '_pairBlend_P')
        cmds.connectAttr('Musical_Articulation.musical_articulation', item + '_pairBlend_M_P.weight')
        cmds.connectAttr('Musical_Articulation.musical_articulation', item + '_pairBlend_M_Pnot.weight')
        cmds.connectAttr('Pitch_Sensitivity.pitch_sensitivity', item + '_pairBlend_P.weight')
        cmds.connectAttr(item + '_pairBlend_M_P.outTranslateX', item + '_pairBlend_P.inTranslateX2')
        cmds.connectAttr(item + '_pairBlend_M_Pnot.outTranslateX', item + '_pairBlend_P.inTranslateX1')

        # Now, here’s the important change:
        # Instead of blindly connecting the pairBlend output to the slider attribute,
        # we check if there’s an existing connection and, if so, blend the two.
        if item not in ["JaliJoystick_Jaw", "JaliJoystick_Lip"]:
            target_attr = item + '.translate.translateY'
            new_source = item + '_pairBlend_P.outTranslate.outTranslateX'
            blend_name = item + '_blendExisting'
            connect_with_blend(target_attr, new_source, blend_name, blend_weight=0.5)
        else:
            # For joystick sliders, use a slightly different attribute naming
            target_attr = item.split("_")[0] + "." + item.split("_")[1]
            new_source = item + '_pairBlend_P.outTranslate.outTranslateX'
            connect_with_blend(target_attr, new_source, item + '_blendExisting', blend_weight=0.5)

        cmds.createNode('animCurveTL', n=item + '_M_P')
        cmds.createNode('animCurveTL', n=item + '_Mnot_P')
        cmds.createNode('animCurveTL', n=item + '_M_Pnot')
        cmds.createNode('animCurveTL', n=item + '_Mnot_Pnot')

        cmds.connectAttr(item + '_M_P.output', item + '_pairBlend_M_P.inTranslateX2')
        cmds.connectAttr(item + '_Mnot_P.output', item + '_pairBlend_M_P.inTranslateX1')
        cmds.connectAttr(item + '_M_Pnot.output', item + '_pairBlend_M_Pnot.inTranslateX2')
        cmds.connectAttr(item + '_Mnot_Pnot.output', item + '_pairBlend_M_Pnot.inTranslateX1')

    # Process viseme sliders (vowel modifiers)
    vowel_mod_sliders = [["Dimple", "Dimple"], ["Pucker", "Pucker"],
                         ["Ee_pointer", "lipCornerPull"], ["Ee_pointer", "lipStretch"],
                         ["Eh_pointer", "lipCornerPull"], ["Eh_pointer", "lipStretch"],
                         ["Oo_pointer", "lipPucker"], ["U_pointer", "lipPucker"]]
    for item in list(vowel_mod_sliders):
        # Delete our previous nodes (if any)
        for suffix in ['_M', '_Mnot']:
            try:
                cmds.delete(item[0] + "_" + item[1] + suffix)
            except:
                pass
        try:
            cmds.delete('pairBlend', n=item[0] + "_" + item[1] + '_pairBlend_M')
        except:
            pass

        # Create the pairBlend node and animCurves for the viseme slider
        cmds.createNode('pairBlend', n=item[0] + "_" + item[1] + '_pairBlend_M')
        cmds.connectAttr('Musical_Articulation.musical_articulation', item[0] + "_" + item[1] + '_pairBlend_M.weight')
        cmds.createNode('animCurveTL', n=item[0] + "_" + item[1] + '_M')
        cmds.createNode('animCurveTL', n=item[0] + "_" + item[1] + '_Mnot')
        cmds.connectAttr(item[0] + "_" + item[1] + '_M.output', item[0] + "_" + item[1] + '_pairBlend_M.inTranslateX2')
        cmds.connectAttr(item[0] + "_" + item[1] + '_Mnot.output',
                         item[0] + "_" + item[1] + '_pairBlend_M.inTranslateX1')
        # *** NEW: For viseme sliders, remove any existing connections before connecting
        target_attr = item[0] + "." + item[1]
        replace_existing_connection(target_attr)
        cmds.connectAttr(item[0] + "_" + item[1] + '_pairBlend_M.outTranslate.outTranslateX', target_attr)

def gen_mvp_curves(input_file):
    with open(input_file) as f:
        data = json.load(f)
    data = json.loads(data)

    # inputs (the same sets as before)
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

    # Clear keyframes (unchanged)
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

    # Set keyframes for the viseme sliders (no changes here)
    for i in range(len(viseme_lists_M_Pnot)):
        node = viseme_lists_M_Pnot[i] + "_M_Pnot"
        for pt in viseme_intervals_M_Pnot[i]:
            cmds.setKeyframe(node, v=pt[1], t=pt[0] * fps)
    for i in range(len(viseme_lists_M_Pnot)):
        node = viseme_lists_M_P[i] + "_M_P"
        for pt in viseme_intervals_M_P[i]:
            cmds.setKeyframe(node, v=pt[1], t=pt[0] * fps)
    for i in range(len(viseme_lists_M_Pnot)):
        node = viseme_lists_Mnot_P[i] + "_Mnot_P"
        for pt in viseme_intervals_Mnot_P[i]:
            cmds.setKeyframe(node, v=pt[1], t=pt[0] * fps)
    for i in range(len(viseme_lists_M_Pnot)):
        node = viseme_lists_Mnot_Pnot[i] + "_Mnot_Pnot"
        for pt in viseme_intervals_Mnot_Pnot[i]:
            cmds.setKeyframe(node, v=pt[1], t=pt[0] * fps)

    # Process jaw and lip keyframes as before
    slider = "JaliJoystick"
    attribute = "Jaw"
    for i in range(len(ja_pts)):
        cmds.setKeyframe(slider + "_Jaw_M_P", v=ja_pts[i][1], t=ja_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Jaw_Mnot_P", v=ja_pts[i][1], t=ja_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Jaw_M_Pnot", v=ja_pts[i][1], t=ja_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Jaw_Mnot_Pnot", v=ja_pts[i][1], t=ja_pts[i][0] * fps)
    slider = "JaliJoystick"
    attribute = "Lip"
    for i in range(len(li_pts)):
        cmds.setKeyframe(slider + "_Lip_M_P", v=li_pts[i][1], t=li_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Lip_Mnot_P", v=li_pts[i][1], t=li_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Lip_M_Pnot", v=li_pts[i][1], t=li_pts[i][0] * fps)
        cmds.setKeyframe(slider + "_Lip_Mnot_Pnot", v=li_pts[i][1], t=li_pts[i][0] * fps)

    # Throat and vibrato parts remain unchanged...
    throat_movement = data["throat"]
    for i in range(len(throat_movement)):
        for k in range(len(throat_movement[i])):
            cmds.setKeyframe("CNT_HYOID", at="Hyoid_inOut", v=throat_movement[i][k][1],
                             t=throat_movement[i][k][0] * fps)
            cmds.setKeyframe("CNT_HYOID", at="Hyoid_downUp", v=throat_movement[i][k][1],
                             t=throat_movement[i][k][0] * fps)

    if True:
        vib_intervals = data["vib"]
        slider = "JaliJoystick"
        attribute = "Jaw"
        for i in range(len(vib_intervals)):
            starting_frame = vib_intervals[i][0] * fps
            ending_frame = vib_intervals[i][1] * fps

            vibrato_frequency = 10  # 5 times per second (as per comment)
            vibrato_height_initial = 0
            vibrato_height_final = 0.6

            vibrato_dire = -1
            t = starting_frame
            step_size = int(fps / vibrato_frequency)
            offsets = []
            while t <= ending_frame:
                offset = cmds.getAttr(slider + '.' + attribute, t=t)
                offsets.append(offset)
                t += step_size
            t = starting_frame
            counter = 0
            while t <= ending_frame:
                vibrato_height = vibrato_height_initial + (vibrato_height_final - vibrato_height_initial) * (
                    t - starting_frame) / (ending_frame - starting_frame)
                cmds.setKeyframe(slider + "_Jaw_M_P", v=offsets[counter] + vibrato_height * vibrato_dire, t=t)
                cmds.setKeyframe(slider + "_Jaw_Mnot_P", v=offsets[counter] + vibrato_height * vibrato_dire, t=t)
                t += step_size
                vibrato_dire *= -1
                counter += 1
            cmds.setKeyframe(slider + "_Jaw_M_P", v=offsets[0], t=t)
            cmds.setKeyframe(slider + "_Jaw_Mnot_P", v=offsets[0], t=t)

    modification_sliders, modification_ctrl_pts = data["vowel_mod_M"]
    for i in range(len(modification_sliders)):
        for j in range(len(modification_ctrl_pts[i])):
            cmds.setKeyframe(modification_sliders[i][0] + "_" + modification_sliders[i][1] + "_M",
                             v=modification_ctrl_pts[i][j][1],
                             t=modification_ctrl_pts[i][j][0] * fps)
    modification_sliders, modification_ctrl_pts = data["vowel_mod_M_not"]
    for i in range(len(modification_sliders)):
        for j in range(len(modification_ctrl_pts[i])):
            cmds.setKeyframe(modification_sliders[i][0] + "_" + modification_sliders[i][1] + "_Mnot",
                             v=modification_ctrl_pts[i][j][1],
                             t=modification_ctrl_pts[i][j][0] * fps)
    print("completed " + input_file)

gen_mvp_curves(input_file)
