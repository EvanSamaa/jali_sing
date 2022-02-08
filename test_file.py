from util.sound_processing import *
from util.SongDataStructure import *
import os


if __name__ == "__main__":
    dataset = ["child_in_time_1_for_mfa", "I_dont_love_you_for_mfa", "rolling_in_the_deep_for_mfa"]
    data_set_path = "E:/MASC/alignment_test/"
    output_path = "E:/MASC/alignment_test/output_text_grids"
    for data in dataset:
        sound_path = os.path.join(data_set_path, data + ".wav")
        script_path = os.path.join(data_set_path, data + ".txt")
        lyric = Minimal_song_data_structure(sound_path, script_path, alignment_type="visemes")
        lyric.compute_self_viseme_alignment()
        lyric.write_textgrid(output_path, data + "_viseme")