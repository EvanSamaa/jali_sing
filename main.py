import json
from util.jali_curve_generation import *
from util.ioUtil import get_wav_from_video
if __name__ == "__main__":
    #
    # file_dir = "F:/MASC/Jali_sing/Revision/Ultimate_heatmap_list/JERRY/JALI/ALL_OF_ME"
    # # song = Minimal_song_data_structure(file_dir+".wav", file_dir+".txt", )
    # # song.compute_self_phoneme_alignment()
    # # song.write_textgrid("F:/MASC/Jali_sing/Revision/Ultimate_heatmap_list/JERRY/JALI/", "ALL_OF_ME")
    # j = JaliVoCa_animation(file_dir + ".wav", file_dir + ".TextGrid", "F:/MASC/Jali_sing/Revision/Ultimate_heatmap_list/JERRY/JALI/ALL_OF_ME.json")
    # j.generate_curves()
    # A[2]
    file_dir = "F:/MASC/Jali_sing/Revision/Artist Editted Video/Free_vocal"
    # song = Minimal_song_data_structure(file_dir+".wav", file_dir+".txt", )
    # song.compute_self_phoneme_alignment()
    # song.write_textgrid("F:/MASC/Jali_sing/Revision/Artist Editted Video/", "Free_vocal_raw")
    j = JaliVoCa_animation(file_dir + ".wav", file_dir + ".TextGrid", "F:/MASC/Jali_sing/Revision/Artist Editted Video/Free_vocal_MVP.json")
    j.generate_curves()

    # file_dir = "F:\\MASC\\Jali_sing\\Revision\\Lip Sync live performances\\wrecking_ball\\"
    # j = JaliVoCa_animation(file_dir + "audio.wav", file_dir + "audio.TextGrid", file_dir + "jali_MVP.json")
    # j.generate_curves()
