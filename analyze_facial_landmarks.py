import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

def display_landmark(landmark_arr, fps):
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    def update(i):
        label = 'timestep {0}'.format(i)
        print(label)
        # Update the line and the axes (with a new xlabel). Return a tuple of
        # "artists" that have to be redrawn for this frame.
        landmark_arr_i = landmark_arr[i]
        fig.clf()
        ax = plt.scatter(landmark_arr_i[:, 0], landmark_arr_i[:, 1])
        return ax
    i = 1
    landmark_arr_i = landmark_arr[0]
    ax.scatter(landmark_arr_i[:, 0], landmark_arr_i[:, 1])
    anim = FuncAnimation(fig, update, frames=np.arange(0, landmark_arr_i.shape[0]), interval=25)

    plt.show()

def simplify_media_pipe_landmarks(face_arr):
    return 0


if __name__ == "__main__":
    landmark_data_path = "E:\\MASC\\facial_data_analysis_videos\\12\\video\\2D_mediapipe_landmark.npy"
    landmark_data = np.load(landmark_data_path)
    display_landmark(landmark_data, 32)
