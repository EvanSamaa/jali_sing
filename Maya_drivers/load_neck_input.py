import pickle as pkl
import math
import json

        
        
def load_head(file_path):
    # load the file
    with open(file_path, 'rb') as f:
        data = pkl.load(f)
    
    # head data is an array of tuple with each tuble of the form [t, x, y, z]
    head_data = data["head_frames"]
    
    # iterate through the list and keyframe x, y, z to CNT_NECK5.rotateX, CNT_NECK5.rotateY, CNT_NECK5.rotateZ 
    fps = mel.eval('float $fps = `currentTimeUnitToFPS`')
    scaleee = 0.3
    for i in range(0, len(head_data)):
        # use maya's setKeyframe command to keyframe the values
        cmds.setKeyframe("CNT_NECK5.rotateX", value=head_data[i][1] * scaleee, t=head_data[i][0] * fps)
        cmds.setKeyframe("CNT_NECK5.rotateY", value=head_data[i][2] * scaleee, t=head_data[i][0] * fps)
        cmds.setKeyframe("CNT_NECK5.rotateZ", value=head_data[i][3] * scaleee, t=head_data[i][0] * fps)
        
    
    
load_head("C:/Users/evansamaa/Downloads/evan_neck_rotations.pkl")
# load_gaze("F:/MASC/JALI_gaze/for_non_conversational/video_360/office_stanford_non_conversational.pkl", "jali")
