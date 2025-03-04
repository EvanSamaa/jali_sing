import cv2 as cv
import mediapipe as mp
import numpy as np
import math
import json
from tqdm import tqdm
from scipy.spatial.transform import Rotation
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
import sys

# Make sure your custom modules are importable.
sys.path.insert(0, "/Users/evanpan/Desktop/EvanToolBox/Utils")
sys.path.insert(0, "C:/Users/evan1/Documents/GitHub/EvansToolBox/Utils")

from Geometry_Util import rotation_matrix_from_vectors, ObjLoader
# (Assuming Video_analysis_utils is not needed for just computing rotations)

def compute_head_rotations(video_path, canonical_face_path, mapping_path, image_mode=False):
    """
    Given:
      - video_path: path to the video file
      - canonical_face_path: path to an OBJ file for the canonical face model
      - mapping_path: path to a JSON file that maps mediapipe landmarks to semantic parts
      - image_mode: if True, face detection is performed on every frame (less efficient),
                    otherwise, tracking is used between frames.
                    
    This function:
      1. Reads the video and extracts raw facial landmarks (478 points per frame) using MediaPipe.
      2. Loads the mediapipe semantic mapping to determine which landmarks are used for the neutral alignment.
      3. Loads the canonical face (via ObjLoader) and flips its Y‐axis (if needed).
      4. For each frame, uses a Procrustes analysis to compute a rotation matrix that best aligns
         the detected landmarks (at indices specified by the mapping) to the canonical face.
      5. Converts the rotation matrices into Euler angles (pitch, yaw, roll) in degrees.
      
    Returns:
       rotation_angles: a NumPy array of shape (num_frames, 3) containing [pitch, yaw, roll] per frame.
    """

    # ---------------------------
    # Helper functions (internal)
    # ---------------------------
    def procrustes_analysis(X, Y):
        """
        Given two sets of points X and Y (each of shape (M, N)) finds R, c, t that minimizes
            || c * R @ X + t - Y ||^2.
        Returns the rotation matrix R, scale c, and translation t (as a column vector).
        """
        mu_x = X.mean(axis=1)
        mu_y = Y.mean(axis=1)
        rho2_x = X.var(axis=1).sum()
        # Compute the covariance matrix between X and Y
        cov_xy = 1.0 / X.shape[1] * (Y - np.expand_dims(mu_y, axis=1)) @ (X - np.expand_dims(mu_x, axis=1)).T
        U, D, V_T = np.linalg.svd(cov_xy)
        D = np.diag(D)
        S = np.identity(3)
        if np.linalg.matrix_rank(cov_xy) >= X.shape[0]-1:
            if np.linalg.det(cov_xy) < 0:
                S[-1,-1] = -1
        else:
            if np.linalg.det(U) * np.linalg.det(V_T) < 0:
                S[-1,-1] = -1
        R = U @ S @ V_T
        c = (1.0 / rho2_x) * np.trace(D @ S)
        t = mu_y - c * R @ mu_x
        return R, c, np.expand_dims(t, 1)

    def rotateToNeutral(neutralPose, data, staticIndices, returnRotation=False):
        """
        Align each frame’s landmarks (data, shape: (T, num_landmarks, 3)) to the neutral pose (neutralPose, shape (N, 3))
        using only the landmarks specified by staticIndices (list of indices).
        If returnRotation is True, also return the list of rotation matrices (one per frame).
        """
        T = data.shape[0]
        outData = np.zeros(data.shape)
        R_out = []
        for i in range(T):
            # Get the landmarks for the current frame at the indices we want to use
            frame_t = data[i, staticIndices]
            # Perform Procrustes analysis aligning frame_t to the corresponding neutral landmarks
            R, c, t = procrustes_analysis(frame_t.T, neutralPose[staticIndices].T)
            if returnRotation:
                R_out.append(R)
            # Apply the computed transformation to all landmarks of the frame
            outData[i] = (c * R @ data[i].T + t).T
        if returnRotation:
            return outData, R_out
        else:
            return outData

    # ---------------------------
    # PART 1: Extract raw landmarks via MediaPipe Face Mesh
    # ---------------------------
    mp_face_mesh = mp.solutions.face_mesh
    raw_landmark_output = []

    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file:", video_path)
        return None
    fps = cap.get(cv.CAP_PROP_FPS)
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=total_frames, desc="Extracting landmarks")
    with mp_face_mesh.FaceMesh(static_image_mode=image_mode,
                               max_num_faces=1,
                               min_detection_confidence=0.5,
                               refine_landmarks=True) as face_mesh:
        while cap.isOpened():
            ret, image = cap.read()
            if not ret:
                break
            # Process the image with MediaPipe (it expects RGB)
            results = face_mesh.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
            if results.multi_face_landmarks:
                # Use the first detected face
                face_landmarks = results.multi_face_landmarks[0].landmark
                # Create an array of shape (478, 3)
                pts = np.zeros((478, 3))
                for i_pt, lm in enumerate(face_landmarks):
                    pts[i_pt, 0] = lm.x
                    pts[i_pt, 1] = lm.y
                    pts[i_pt, 2] = lm.z
                raw_landmark_output.append(pts)
            else:
                # If no face is detected, append zeros
                raw_landmark_output.append(np.zeros((478, 3)))
            pbar.update(1)
    pbar.close()
    cap.release()
    raw_landmark_output = np.array(raw_landmark_output)  # shape: (num_frames, 478, 3)

    # ---------------------------
    # PART 2: Load mapping and canonical face
    # ---------------------------
    # Load mediapipe semantic mapping (JSON)
    with open(mapping_path, "r") as f:
        mapping = json.load(f)
    # Determine static landmark indices (for procrustes alignment) from the mapping.
    # Here we assume the mapping file has keys "nose" with "dorsum" and "tipLower", and "additional_anchors".
    staticLandmarkIndices = mapping["nose"]["dorsum"] + mapping["nose"]["tipLower"] + mapping["additional_anchors"]
    # (The code below also builds a larger set (keypointIndicies) but we only need the static ones for rotation)
    # keypointIndicies = (mapping["nose"]["dorsum"] + mapping["nose"]["tipLower"] +
    #                     mapping["additional_anchors"] + mapping["brow"]["rightLower"] +
    #                     mapping["brow"]["rightUpper"] + mapping["brow"]["leftUpper"] +
    #                     mapping["brow"]["leftLower"] + mapping["eye"]["right"] + mapping["eye"]["left"] +
    #                     mapping["lips"]["inner"] + mapping["lips"]["outer"])

    # Load canonical face model using your ObjLoader
    face = ObjLoader(canonical_face_path)
    # Flip the Y axis if necessary (as done in your old code)
    face.vertices[:, 1] = -face.vertices[:, 1]

    # ---------------------------
    # PART 3: Compute Rotation via Procrustes Analysis
    # ---------------------------
    # Rotate each frame’s landmarks to the neutral canonical face using only the static indices.
    # Return the rotation matrices.
    _, rotation_matrices = rotateToNeutral(face.vertices, raw_landmark_output, staticLandmarkIndices, returnRotation=True)
    rotation_matrices = np.array(rotation_matrices)  # list of (3x3) matrices

    # Convert the rotation matrices to Euler angles (using "xyz" order, in degrees)
    rotations = Rotation.from_matrix(rotation_matrices)
    rotation_angles = rotations.as_euler("xyz", degrees=True)
    # rotation_angles will be an array of shape (num_frames, 3) containing [pitch, yaw, roll] per frame.

    # normalize to 30 fps
    target_fps = 30
    original_fps = fps
    
    old_x = np.arange(0, len(rotation_angles))
    new_x = np.linspace(0, len(rotation_angles), int(len(rotation_angles) * target_fps / original_fps))
    f = interp1d(old_x, rotation_angles, axis=0, bounds_error=False, fill_value="extrapolate")
    rotation_angles = f(new_x)
    
    return rotation_angles

def clean_head_rotations(rotations, window_length=15, polyorder=2):
    # dealing with the discontinuity in Euler angles
    for i in range(len(rotations)):
        for j in range(0, 3):
            val = rotations[i, j]
            if val < -90:
                rotations[i, j] = val + 180
            elif val > 90:
                rotations[i, j] = val - 180
    
    # apply smoothing using savgol filter
    rotations = savgol_filter(rotations, window_length, polyorder, axis=0)
    
    return rotations            

def output_rotations(rotations, output_path, target_fps=30):
    # Save the cleaned rotations to a JSON file
    output_data = {
        "fps": target_fps,
        "poses": []
    }
    for t, angles in enumerate(rotations):
        output_data["poses"].append({
            "timestamp": t / target_fps,
            "pitch": float(angles[0]),
            "yaw": float(angles[1]),
            "roll": float(angles[2])
        })
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=4)    
    print("Saved head pose data to", output_path)

def normalize_rotations(rotations):
    mean = rotations.mean(axis=0)
    std = rotations.std(axis=0)
    return (rotations - mean) / std


# Example usage:
if __name__ == "__main__":
    video_path = "C:/Users/evan1/Desktop/music_companion/Ashish_Mario/MySlate_1_iPhone.mov"
    output_path = "C:/Users/evan1/Desktop/music_companion/Ashish_Mario/MySlate_1_iPhone_sheer_normalzation.json"
    
    canonical_face_path = "C:/Users/evan1/Documents/GitHub/EvansToolBox/Video_Annotation/models/mediapipe_canonical_face_mesh.obj"
    mapping_path = "C:/Users/evan1/Documents/GitHub/EvansToolBox/Video_Annotation/models/mediapipe_emantic_mapping.json"
    
    
    rotations = compute_head_rotations(video_path, canonical_face_path, mapping_path, image_mode=False)
    smoothed_rotations = clean_head_rotations(rotations, 17, 2)
    normalized_rotations = normalize_rotations(smoothed_rotations) * 5
    
    output_rotations(normalized_rotations, output_path)