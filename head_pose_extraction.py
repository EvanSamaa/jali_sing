import cv2
import dlib
import numpy as np
import math
import json
import sys
from scipy.interpolate import interp1d

# ---------------------------
# SETTINGS & MODEL POINTS
# ---------------------------
PREDICTOR_PATH = "C:/Users/evan1/Documents/JALI_sing_stuff/jali_sing/models/shape_predictor_68_face_landmarks.dat"

# 3D model points of key facial landmarks in some arbitrary world scale.
# (nose tip, chin, left eye corner, right eye corner, left mouth corner, right mouth corner)
model_points = np.array([
    (0.0, 0.0, 0.0),             # Nose tip
    (0.0, -330.0, -65.0),        # Chin
    (-225.0, 170.0, -135.0),     # Left eye left corner
    (225.0, 170.0, -135.0),      # Right eye right corner
    (-150.0, -150.0, -125.0),    # Left mouth corner
    (150.0, -150.0, -125.0)      # Right mouth corner
], dtype=np.float64)

# ---------------------------
# ONE EURO FILTER PARAMETERS
# ---------------------------
ONE_EURO_MIN_CUTOFF = 0.5  # Minimum cutoff frequency (Hz)
ONE_EURO_BETA = 0.1        # Speed coefficient; higher => more responsive (less smoothing)
ONE_EURO_D_CUTOFF = 1.0    # Derivative cutoff frequency

# ---------------------------
# ONE EURO FILTER IMPLEMENTATION
# ---------------------------
class OneEuroFilter:
    def __init__(self, freq, min_cutoff=1.0, beta=0.0, d_cutoff=1.0):
        self.freq = freq  # initial frequency (Hz)
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.x_prev = None
        self.dx_prev = 0.0
        self.last_time = None

    def alpha(self, cutoff, dt):
        tau = 1.0 / (2 * np.pi * cutoff)
        return 1.0 / (1.0 + tau / dt)
    
    def filter(self, x, t):
        # Compute time difference
        if self.last_time is None:
            dt = 1.0 / self.freq
        else:
            dt = t - self.last_time
            if dt <= 0:
                dt = 1.0 / self.freq
        self.freq = 1.0 / dt  # update frequency

        # Estimate derivative
        if self.x_prev is None:
            dx = 0.0
        else:
            dx = (x - self.x_prev) / dt

        # Low-pass filter the derivative
        a_d = self.alpha(self.d_cutoff, dt)
        dx_hat = a_d * dx + (1 - a_d) * self.dx_prev

        # Compute the cutoff for the signal
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = self.alpha(cutoff, dt)

        # Low-pass filter the signal
        if self.x_prev is None:
            x_hat = x
        else:
            x_hat = a * x + (1 - a) * self.x_prev

        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.last_time = t

        return x_hat

def one_euro_filter_channel(timestamps, values, freq, min_cutoff, beta, d_cutoff):
    filter_inst = OneEuroFilter(freq, min_cutoff, beta, d_cutoff)
    filtered = []
    for t, x in zip(timestamps, values):
        filtered.append(filter_inst.filter(x, t))
    return np.array(filtered)

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def rotationMatrixToEulerAngles(R):
    """
    Calculates rotation matrix to Euler angles.
    Returns angles (in degrees) in the order: [pitch, yaw, roll]
    Assumes rotations about X (pitch), Y (yaw), Z (roll).
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

def get_head_pose(shape, img_size):
    """
    Given a dlib shape object and image size, computes head pose via solvePnP.
    Uses 6 landmarks: nose tip (30), chin (8), left eye corner (36), right eye corner (45),
    left mouth corner (48) and right mouth corner (54).
    Returns Euler angles [pitch, yaw, roll] in degrees.
    """
    image_points = np.array([
        (shape.part(30).x, shape.part(30).y),  # Nose tip
        (shape.part(8).x, shape.part(8).y),      # Chin
        (shape.part(36).x, shape.part(36).y),    # Left eye left corner
        (shape.part(45).x, shape.part(45).y),    # Right eye right corner
        (shape.part(48).x, shape.part(48).y),    # Left mouth corner
        (shape.part(54).x, shape.part(54).y)     # Right mouth corner
    ], dtype=np.float64)
    
    focal_length = img_size[1]  # approximate focal length
    center = (img_size[1] / 2, img_size[0] / 2)
    camera_matrix = np.array([
         [focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]
    ], dtype=np.float64)
    dist_coeffs = np.zeros((4,1))  # assume no lens distortion

    success, rotation_vector, translation_vector = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)
    if not success:
        return np.array([0, 0, 0])
    R, _ = cv2.Rodrigues(rotation_vector)
    euler_angles = rotationMatrixToEulerAngles(R)
    return euler_angles

def process_video(video_path, output_json="head_pose.json", target_fps=30):
    # Initialize dlib detector and predictor.
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file:", video_path)
        return

    orig_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Original FPS: {orig_fps}")
    poses = []
    timestamps = []

    frame_idx = 0
    while True:
        print("processing frame", frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dets = detector(gray, 0)
        if len(dets) > 0:
            shape = predictor(gray, dets[0])
            pose = get_head_pose(shape, frame.shape)
        else:
            pose = np.array([0, 0, 0])
        t = frame_idx / orig_fps  # timestamp in seconds
        timestamps.append(t)
        poses.append(pose)
        frame_idx += 1

    cap.release()
    poses = np.array(poses)  # shape: (num_frames, 3)

    # ---------------------------
    # RESAMPLE TO TARGET FPS
    # ---------------------------
    total_duration = timestamps[-1] if timestamps else 0
    new_timestamps = np.arange(0, total_duration, 1 / target_fps)
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

    # --- Flip pitch if near ±90 (to avoid discontinuities) ---
    for i in range(len(cleaned)):
        pitch = cleaned[i, 0]
        if pitch < -90:
            cleaned[i, 0] = pitch + 180
        elif pitch > 90:
            cleaned[i, 0] = pitch - 180

    # ---------------------------
    # APPLY ONE EURO FILTER TO EACH CHANNEL
    # ---------------------------
    filtered_pitch = one_euro_filter_channel(new_timestamps, cleaned[:, 0], target_fps,
                                               ONE_EURO_MIN_CUTOFF, ONE_EURO_BETA, ONE_EURO_D_CUTOFF)
    filtered_yaw = one_euro_filter_channel(new_timestamps, cleaned[:, 1], target_fps,
                                             ONE_EURO_MIN_CUTOFF, ONE_EURO_BETA, ONE_EURO_D_CUTOFF)
    filtered_roll = one_euro_filter_channel(new_timestamps, cleaned[:, 2], target_fps,
                                              ONE_EURO_MIN_CUTOFF, ONE_EURO_BETA, ONE_EURO_D_CUTOFF)
    filtered = np.column_stack((filtered_pitch, filtered_yaw, filtered_roll))

    # ---------------------------
    # SAVE TO JSON
    # ---------------------------
    output_data = {
        "fps": target_fps,
        "poses": []
    }
    for t, angles in zip(new_timestamps, filtered):
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
    video_path = "C:/Users/evan1/Desktop/music_companion/die_with_a_smile/video_source_chorus.mov"
    output_path = "C:/Users/evan1/Desktop/music_companion/die_with_a_smile/video_source_chorus.json"
    process_video(video_path, output_path)
