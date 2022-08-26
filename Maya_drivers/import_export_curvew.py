import maya.cmds as cmds
import json
import sys
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
            cmds.connectAttr(item + '_pairBlend_P.outTranslate.outTranslateX', item.split("_")[0] + "." +  item.split("_")[1], force=True)
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
        cmds.connectAttr(item[0] + "_" + item[1] + '_Mnot.output', item[0] + "_" + item[1] + '_pairBlend_M.inTranslateX1')
        cmds.connectAttr(item[0] + "_" + item[1] + '_pairBlend_M.outTranslate.outTranslateX', item[0] + "." + item[1])

def get_all_slider_attributes():
    out = []
    objects = ["CNT_UPFACE", "CNT_MIDFACE", "CNT_LOFACE", "loLids", "blink", "CNT_BOTH_EYES",
    "CNT_JAW", "jNeck_ctl", "SPEECH_PHONEMES", "SPEECH_NOJAW", "JaliJoystick"]
    for object in objects:
        attrs = cmds.listAttr(object, k=True)
        for attr in attrs:
            out.append(object+"."+attr.encode('ascii', 'ignore'))
    return out
def Exporting_JALI(path):
    saved_path = path
    output = {}
    def exporting(*args):
        path_name = cmds.textField(saved_path, text=True, query=True)     
        attrs = get_all_slider_attributes()
        for item in attrs:
            kf_t = cmds.keyframe(item, query=True)
            output[item] = {}
            if not kf_t is None:
                kf_v = []
                for tttt in kf_t:
                    # C:/Users/evan1/Documents/JALI_sing_stuff/jali_sing/Maya_drivers/test.json
                    # C:/Users/evansamaa/Desktop/jali_sing/Maya_drivers/test.json
                    kf_v.append(cmds.getAttr(item, t=tttt))
                output[item]["t"] = kf_t
                output[item]["v"] = kf_v
            else:
                output[item]["t"] = []
                output[item]["v"] = []
        with open(path_name, "w") as fp:
            json.dump(output, fp)          
    return exporting
def Exporting_Vocal(path):
    saved_path = path
    def exporting(*args):
        output = {}
        path_name = cmds.textField(saved_path, text=True, query=True)
        curve_suffix = ["_M_P", "_Mnot_P", "_M_Pnot", "_Mnot_Pnot"]
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
        slider_names = list(JALI_SLIDERS_SET)
        for i in range(0, len(slider_names)):
            for curve_type in curve_suffix:
                item_name = slider_names[i]+curve_type
                kf_t = cmds.keyframe(item_name, query=True)
                output[item_name] = {}
                if not kf_t is None:
                    kf_v = []
                    for tttt in kf_t:
                        kf_v.append(cmds.keyframe(item_name, query=True, eval=True, time=(tttt, tttt))[0])
                    output[item_name]["t"] = kf_t
                    output[item_name]["v"] = kf_v
                else:
                    output[item_name]["t"] = []
                    output[item_name]["v"] = []
        vowel_mod_sliders = [["Dimple", "Dimple"], ["Pucker", "Pucker"],
                         ["Ee_pointer", "lipCornerPull"], ["Ee_pointer", "lipStretch"],
                         ["Eh_pointer", "lipCornerPull"], ["Eh_pointer", "lipStretch"],
                         ["Oo_pointer", "lipPucker"], ["U_pointer", "lipPucker"]]
        for item in list(vowel_mod_sliders):
            for suffix in ["_M", "_Mnot"]:
                n = item[0] + "_" + item[1] + suffix
                kf_t = cmds.keyframe(n, query=True) 
                output[item_name] = {}
                if not kf_t is None:
                    kf_v = []
                    for tttt in kf_t:
                        kf_v.append(cmds.keyframe(n, query=True, eval=True, time=(tttt, tttt))[0])
                    output[item_name]["t"] = kf_t
                    output[item_name]["v"] = kf_v
                else:
                    output[item_name]["t"] = []
                    output[item_name]["v"] = []
        slider = "JaliJoystick"
        attributessss = ["_Jaw", "_Lip"]
        for att in attributessss:
            for suffix in curve_suffix:
                item_name = slider + att + suffix
                kf_t = cmds.keyframe(item_name, query=True)
                output[item_name] = {}
                if not kf_t is None:
                    kf_v = []
                    for tttt in kf_t:
                        kf_v.append(cmds.keyframe(item_name, query=True, eval=True, time=(tttt, tttt))[0])
                    output[item_name]["t"] = kf_t
                    output[item_name]["v"] = kf_v
                else:
                    output[item_name]["t"] = []
                    output[item_name]["v"] = []
            
            
        with open(path_name, "w") as fp:
            json.dump(output, fp)  
                         
    return exporting
def Importing_JALI(path, model_prefix):
    saved_path = path
    saved_model_prefix = model_prefix
    def importing(*args):
        path_name = cmds.textField(saved_path, text=True, query=True)    
        prefix_name = cmds.textField(saved_model_prefix, text=True, query=True)
        if prefix_name == " ":
            prefix_name = ""
        with open(path_name) as f:
            motion = json.load(f)
        for key in motion.keys():
            t = motion[key]["t"]
            v = motion[key]["v"]
            cmds.cutKey(key)
            for i in range(0, len(t)):
                cmds.setKeyframe(prefix_name+key, v=v[i], t=t[i])
    return importing
def Importing_Vocal(path, model_prefix):
    init_blend_nodes()
    saved_path = path
    saved_model_prefix = model_prefix
    def importing(*args):
        path_name = cmds.textField(saved_path, text=True, query=True)     
        prefix_name = cmds.textField(saved_model_prefix, text=True, query=True)
        if prefix_name == " ":
            prefix_name = ""
        with open(path_name) as f:
            motion = json.load(f)
        for key in motion.keys():
            t = motion[key]["t"]
            v = motion[key]["v"]
            cmds.cutKey(key)
            for i in range(0, len(t)):
                cmds.setKeyframe(prefix_name+key, v=v[i], t=t[i])
    return importing    
cmds.window(width=300, title="VOCAL_import_export_tool")
cmds.columnLayout(adjustableColumn=True)
label1 = cmds.text("file path:")
path = cmds.textField(text="")
label2 = cmds.text("prefix_name:")
prefix_name= cmds.textField(text="")
cmds.button(label='Export_Jali', command=Exporting_JALI(path))
cmds.button(label='Export_Vocal', command=Exporting_Vocal(path))
cmds.button(label='Import_Jali', command=Importing_JALI(path, prefix_name))
cmds.button(label='Import_Vocal', command=Importing_Vocal(path, prefix_name))
cmds.showWindow()