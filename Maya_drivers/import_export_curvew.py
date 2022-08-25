import maya.cmds as cmds
import json
import sys

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
                    kf_v.append(cmds.getAttr(item, t=tttt))
                output[item]["t"] = kf_t
                output[item]["v"] = kf_v
            else:
                output[item]["t"] = []
                output[item]["v"] = []
        with open(path_name, u'w') as fp:
            json.dump(output, fp)          
    return exporting
def Exporting_Vocal(path):
    saved_path = path
    def exporting(*args):
        pass
        
    return exporting
def Importing_JALI(path):
    saved_path = path
    def importing(*args):
        path_name = cmds.textField(saved_path, text=True, query=True)     
        with open(path_name) as f:
            motion = json.load(f)
        for key in motion.keys():
            t = motion[key]["t"]
            v = motion[key]["v"]
            print(t, v)
            for i in range(0, len(t)):
                cmds.setKeyframe(key, v=v[i], t=t[i])
    return importing
def Importing_Vocal(path):
    saved_path = path
    def importing(*args):
        pass
    return importing
        
cmds.window(width=300, title="VOCAL_import_export_tool")
cmds.columnLayout(adjustableColumn=True)
path = cmds.textField(text="")
cmds.button(label='Export_Jali', command=Exporting_JALI(path))
cmds.button(label='Export_Vocal', command=Exporting_Vocal(path))
cmds.button(label='Import_Jali', command=Importing_JALI(path))
cmds.button(label='Import_Vocal', command=Importing_Vocal(path))
cmds.showWindow()