import json
from util.jali_curve_generation import *

if __name__ == "__main__":
    dir = "F:/MASC/Jali_sing/validation/faceware session 2022 Apr 1st/julie_takes/rap_jali/"
    # tim = Minimal_song_data_structure(dir+"rap.wav", dir+"rap.txt")
    # tim.compute_self_phoneme_alignment()
    # tim.write_textgrid(dir, "rap_alignment")
    j = JaliVoCa_animation(dir + "rap.wav", dir + "rap_alignment.TextGrid", dir + "jali_MVP.json")
    j.generate_curves()