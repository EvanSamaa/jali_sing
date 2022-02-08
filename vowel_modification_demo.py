import numpy as np
import json
from matplotlib import pyplot as plt
import os
from scipy.interpolate import interp1d, splrep, splev
from models.vowel_modification_detector import vowel_mod_detector
import librosa
import argparse

def detect(aud):
    vowel_mod = vowel_mod_detector()
    # aud = librosa.load(audio_file_path, sr=44100)[0]
    vowel_mod_out, vowel_mod_out_coarse = vowel_mod(aud)
    xs = np.linspace(0, vowel_mod_out_coarse.shape[0]/44100.0, vowel_mod_out_coarse.shape[0])
    coarse_vowel_sounds_like_interp = interp1d(xs, vowel_mod_out_coarse, axis=0)
    for i in range(0, 4):
        plt.plot(vowel_mod_out_coarse[:, i], label=["Ah", "Ee or Eh", "Oo or Oh", "silence"][i])
#         plt.plot(np.argmax(out[0, :], axis=1))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An addition program")
    parser.add_argument("-p", "--path", nargs='1', type=str, metavar="file_name", default = None,
                        help="audio path")
    # path = "C:/Users/evansamaa/Desktop/temp/A_O.wav"
    args = parser.parse_args()
    path = args.path
    try:
        aud = librosa.load(path[0], sr=44100)[0]
    except:
        print("file do not exist")
    detect(aud)



