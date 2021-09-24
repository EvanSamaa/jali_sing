from util.yin import yinAlgo
import winsound
import time
import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":
    file = ".//Jali_Experiments\\zombie\\zombie_cover.wav"
    snd = parselmouth.Sound(file)
    # spectrogram = snd.to_spectrogram()
    # mfcc = snd.to_mfcc(15)
    dt = 0.01

    # obtain pitch from the sound file (this is not bad)
    pitch = snd.to_pitch(time_step=dt, pitch_ceiling=1200)
    pitch_arr = []
    for i in range(0, len(pitch.selected_array)):
        pitch_arr.append(pitch.selected_array[i][0])

    # obtain intensity from the sound file
    print(len(pitch_arr))
    intensity = snd.to_intensity(time_step=dt)
    print(intensity.values.shape)