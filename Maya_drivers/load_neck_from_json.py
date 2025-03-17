import json
import maya.cmds as cmds

# --- SETTINGS ---
# Change this path to the location of your JSON file.
json_path = "C:/Users/evan1/Desktop/music_companion/Sue_Winter/MySlate_4_iPhone_sheer_normalzation.json"
SCALE = 0.6
# The names of the controls/attributes you want to drive.
# We assume that:
#   pitch -> jNeck_ctl.jNeck_xRotate
#   yaw   -> jNeck_ctl.jNeck_yRotate
#   roll  -> jNeck_ctl.jNeck_zRotate
attr_map = {
    "pitch": "CNT_NECK.rotateX",
    "yaw":   "CNT_NECK.rotateY",
    "roll":  "CNT_NECK.rotateZ"
}

# --- FUNCTIONS ---
def disconnect_attr(attr):
    """
    Disconnect any incoming connections on a given attribute.
    """
    conns = cmds.listConnections(attr, s=True, plugs=True)
    if conns:
        for src in conns:
            try:
                cmds.disconnectAttr(src, attr)
                print("Disconnected", src, "from", attr)
            except Exception as e:
                print("Error disconnecting", src, "from", attr, ":", e)

def load_json_pose_data(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data

def apply_keyframes(data):
    # Get the JSON's fps value; default to 30 if not present.
    json_fps = data.get("fps", 30)
    poses = data.get("poses", [])
    
    # For our purposes, we'll assume that timestamp is in seconds.
    # We convert time to frame numbers using: frame = timestamp * json_fps.
    # (Adjust if your scene has a different time unit.)
    
    for pose in poses:
        timestamp = pose.get("timestamp", 0)
        frame = timestamp * json_fps
        # Optionally round frame to a reasonable precision:
        frame = round(frame, 3)
        # For each attribute, set a keyframe.
        for key, attr in attr_map.items():
            value = pose.get(key, 0) * SCALE
            cmds.setKeyframe(attr, v=value, t=frame)
            print("Set keyframe on", attr, "at frame", frame, "value:", value)


# --- MAIN SCRIPT ---
def main():
    # 1. Disconnect any nodes currently connected to our controls.
    for attr in attr_map.values():
        disconnect_attr(attr)
    
    # 2. Load the JSON data.
    data = load_json_pose_data(json_path)
    print("Loaded JSON head pose data.")

    # 3. Map per–frame head rotations onto the rig.
    apply_keyframes(data)
    print("Completed applying keyframes from JSON.")

# Execute when running the script:
if __name__ == "__main__":
    main()
