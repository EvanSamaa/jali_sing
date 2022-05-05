import json
from util.jali_curve_generation import *

if __name__ == "__main__":
    dir = "F:\\MASC\\Jali_sing\\Revision\\validation\\faceware session Yannis\\Oh Canada\\jali_sing_stuff\\"
    # tim = Minimal_song_data_structure(dir+"rap.wav", dir+"rap.txt")
    # tim.compute_self_phoneme_alignment()
    # tim.write_textgrid(dir, "rap_alignment")
    j = JaliVoCa_animation(dir + "Ps0_facecam.wav", dir + "Ps1_facecam.TextGrid", dir + "jali_curves_MVP.json")
    j.generate_curves()