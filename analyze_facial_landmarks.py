import numpy as np
import os
from matplotlib import pyplot as plt

def display_landmark(landmark_arr, fps):
    for i in range(0, landmark_arr.shape[0]):
        landmark_arr_i = landmark_arr[i]
        plt.scatter(landmark_arr_i[:, 0], landmark_arr_i[:, 1])
        # plt.scatter(landmark_arr_i[4, 0], landmark_arr_i[4, 1])
        # plt.scatter(landmark_arr_i[98, 0], landmark_arr_i[98, 1])
        # plt.scatter(landmark_arr_i[327, 0], landmark_arr_i[327, 1])
        # plt.show()
        plt.show(block=False)
        plt.pause(0.001)
        plt.close()
def simplify_media_pipe_landmarks(face_arr):
    return 0


if __name__ == "__main__":

    input_videos = ["high vowels.mp4", "low vowels.mp4", "medium vowels.mp4"]
    input_dir = "F:/vowel_in_different_pitch"
    land_marks = []
    avg_face = []
    for vid in input_videos:
        land_marks.append(np.load(os.path.join(os.path.join(input_dir, vid[:-4]), "landmark.npy")))
        avg_face.append(land_marks[-1].mean(axis=0))