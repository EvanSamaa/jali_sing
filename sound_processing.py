import librosa
import pydub
import os
def format_conversion_m4a2wav(file_name:str):
    filename = './Jali_Experiments/Jali_Experiments.{}'
    from pydub import AudioSegment
    audio: pydub.audio_segment.AudioSegment = AudioSegment.from_file(filename.format("wav"))
    audio.export(filename.format("wav"), format="s16be")
    os.remove(filename.format("m4a"))
    return 0

if __name__ == "__main__":
    print("hello world")
    format_conversion_m4a2wav("")

