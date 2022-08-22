import json
from util.jali_curve_generation import *

if __name__ == "__main__":
    # file_dir = "C:/Users/evansamaa/Desktop/temp/Cam02_07_SamCalib_SamJerusalem2"
    # # song = Minimal_song_data_structure(file_dir+".wav", file_dir+".txt", )
    # # song.compute_self_phoneme_alignment()
    # # song.write_textgrid("C:/Users/evansamaa/Desktop/temp/", "Cam02_07_SamCalib_SamJerusalem2.TEXTGRID")
    # j = JaliVoCa_animation(file_dir + ".wav", file_dir + ".TextGrid", "C:/Users/evansamaa/Desktop/temp/jali_MVP.json")
    # j.generate_curves()

    file_dir = "F:\\MASC\\Jali_sing\\Revision\\Lip Sync live performances\\wrecking_ball\\"
    j = JaliVoCa_animation(file_dir + "audio.wav", file_dir + "audio.TextGrid", file_dir + "jali_MVP.json")
    j.generate_curves()
