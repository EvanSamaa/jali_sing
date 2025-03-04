import cv2
import mediapipe as mp
import numpy as np
import json
import math
from scipy.interpolate import interp1d
import sys

# ---------------------------
# SETTINGS & MODEL POINTS
# ---------------------------
# These indices are chosen from MediaPipe Face Mesh:
#   nose tip:         1
#   chin:             152
#   left eye outer:    33
#   right eye outer:  263
#   left mouth corner: 61
#   right mouth corner:291
LANDMARK_IDS = {
    "nose": 1,
    "chin": 152,
    "left_eye": 33,
    "right_eye": 263,
    "left_mouth": 61,
    "right_mouth": 291
}

# 3D model points (in millimeters) for the corresponding facial landmarks.
# These numbers come from a generic head model.
model_points = np.array([
    (0.0, 0.0, 0.0),             # Nose tip
    (0.0, -330.0, -65.0),        # Chin
    (-225.0, 170.0, -135.0),     # Left eye left corner
    (225.0, 170.0, -135.0),      # Right eye right corner
    (-150.0, -150.0, -125.0),    # Left mouth corner
    (150.0, -150.0, -125.0)      # Right mouth corner
], dtype=np.float64)

def rotationMatrixToEulerAngles(R):
    """
    Converts a rotation matrix to Euler angles (pitch, yaw, roll) in degrees.
    Here we assume the order X (pitch), Y (yaw), Z (roll).
    """
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.degrees(np.array([x, y, z]))

def process_video(video_path, output_json="head_pose.json", target_fps=30):
    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                      max_num_faces=1,
                                      refine_landmarks=True,
                                      min_detection_confidence=0.5,
                                      min_tracking_confidence=0.5)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file:", video_path)
        return
    
    orig_fps = cap.get(cv2.CAP_PROP_FPS)
    print("Original FPS:", orig_fps)
    
    poses = []       # will hold [pitch, yaw, roll] per frame
    timestamps = []  # corresponding timestamps in seconds
    
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img_h, img_w, _ = frame.shape
        # Convert image to RGB (MediaPipe expects RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            # Use the first detected face.
            landmarks = results.multi_face_landmarks[0].landmark
            image_points = []
            # Get the six points from the chosen landmark indices.
            for key in ["nose", "chin", "left_eye", "right_eye", "left_mouth", "right_mouth"]:
                idx = LANDMARK_IDS[key]
                lm = landmarks[idx]
                x = lm.x * img_w
                y = lm.y * img_h
                image_points.append((x, y))
            image_points = np.array(image_points, dtype=np.float64)
            
            # Create camera matrix using image dimensions.
            focal_length = img_w  # approximation
            center = (img_w / 2, img_h / 2)
            camera_matrix = np.array([
                [focal_length, 0, center[0]],
                [0, focal_length, center[1]],
                [0, 0, 1]
            ], dtype=np.float64)
            dist_coeffs = np.zeros((4, 1))  # assuming no lens distortion
            
            # Solve the PnP problem
            success, rotation_vector, translation_vector = cv2.solvePnP(
                model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
            if success:
                R, _ = cv2.Rodrigues(rotation_vector)
                euler_angles = rotationMatrixToEulerAngles(R)  # returns [pitch, yaw, roll]
            else:
                euler_angles = np.array([0, 0, 0])
        else:
            # No face found; default to zero rotations.
            euler_angles = np.array([0, 0, 0])
        
        # Record timestamp (in seconds) and pose.
        t = frame_idx / orig_fps
        timestamps.append(t)
        poses.append(euler_angles)
        frame_idx += 1
    
    cap.release()
    face_mesh.close()
    
    poses = np.array(poses)  # shape: (num_frames, 3)
    
    # ---------------------------
    # RESAMPLE TO TARGET FPS
    # ---------------------------
    total_duration = timestamps[-1] if timestamps else 0
    new_timestamps = np.arange(0, total_duration, 1/target_fps)
    resampled = np.zeros((len(new_timestamps), 3))
    for i in range(3):
        resampled[:, i] = np.interp(new_timestamps, timestamps, poses[:, i])
    
    # ---------------------------
    # CLEAN UP THE ANGLES (unwrap discontinuities)
    # ---------------------------
    cleaned = np.zeros_like(resampled)
    for i in range(3):
        rad = np.radians(resampled[:, i])
        unwrapped = np.unwrap(rad)
        cleaned[:, i] = np.degrees(unwrapped)
    
    # ---------------------------
    # SAVE TO JSON
    # ---------------------------
    output_data = {
        "fps": target_fps,
        "poses": []
    }
    for t, angles in zip(new_timestamps, cleaned):
        output_data["poses"].append({
            "timestamp": t,
            "pitch": float(angles[0]),
            "yaw": float(angles[1]),
            "roll": float(angles[2])
        })
    
    with open(output_json, "w") as f:
        json.dump(output_data, f, indent=4)
    print("Saved head pose data to", output_json)

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mediapipe_head_pose.py <path_to_video>")
    else:
        video_path = "C:/Users/evan1/Desktop/music_companion/die_with_a_smile/video_source_chorus.mov"
        output_path = "C:/Users/evan1/Desktop/music_companion/die_with_a_smile/video_source_chorus.json"        
        process_video(video_path, output_path)
