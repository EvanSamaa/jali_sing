import librosa
import pydub
import os
import math
import time
import winsound

NOTES_NAME = ["A", "A#", "B", "C", "C#", "D",
         "D#", "E", "F", "F#", "G", "G#"]
NOTES_DICT = {"A":0, "A#":1, "B":2, "C":3, "C#":4, "D":5,
         "D#":6, "E":7, "F":8, "F#":9, "G":10, "G#":11}
LOWEST_NOTE = 27.50
RESTING_FREQUENCY = 60

SOPRANO = ["C4", "A5"]
MEZZO_SOPRANO = ["A3", "F#5"]
ALTO = ["G3", "E4"]
TENOR = ["C3", "A4"]
BARITONE = ["A2", "F4"]
BASS = ["F2", "E4"]
VOCAL_RANGES = [BASS, BARITONE, TENOR, ALTO, MEZZO_SOPRANO, SOPRANO]



class Music_note():
    def __init__(self, duration, frequency=None, note=None):
        if note is None and frequency is None:
            raise Exception("you must enter either note or frequency")
        elif note is None:
            if frequency < 27.50:
                self.note = "N/A"
                self.frequency = 27.50
            else:
                number = int(math.log2(frequency/LOWEST_NOTE) * 12)
                octive = math.floor(number / 12)
                note_id = number % 12
                self.frequency = LOWEST_NOTE * pow(2, number/12.0)
                self.note = NOTES_NAME[note_id] + "{}".format(octive + 1)
        else:
            try:
                octive = int(note[-1]) - 1
                note_id = NOTES_DICT[note[:-1]]
                self.frequency = LOWEST_NOTE * pow(2, (octive*12+note_id) / 12.0)
                self.note = note
            except:
                self.note = "N/A"
                self.frequency = 0
        self.duration = duration
    def print(self, freq=None):
        if freq is None:
            print("freq = ", self.frequency)
            print("note = {}".format(self.note))
        else:
            number = int(math.log2(freq / LOWEST_NOTE) * 12)
            octive = math.floor(number / 12)
            note_id = number % 12
            print("freq = ", freq)
            print(NOTES_NAME[note_id] + "{}".format(octive + 1))
    def play(self):
        if self.note == "N/A":
            time.sleep(self.duration)
        else:
            winsound.Beep(int(self.frequency), int(self.duration * 1000))

def format_conversion_m4a2wav(file_name:str):
    filename = './Jali_Experiments/Jali_Experiments.{}'
    from pydub import AudioSegment
    audio: pydub.audio_segment.AudioSegment = AudioSegment.from_file(filename.format("wav"))
    audio.export(filename.format("wav"), format="s16be")
    os.remove(filename.format("m4a"))
    return 0

if __name__ == "__main__":
    # format_conversion_m4a2wav("")
    for voc in VOCAL_RANGES:
        print(Music_note(0.1, note=voc[0]).frequency, Music_note(0.1, note=voc[1]).frequency)



