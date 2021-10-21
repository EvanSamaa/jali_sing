import librosa
import os
import math
import time
import winsound
import textgrids
import parselmouth
from scipy.signal import savgol_filter, correlate
import numpy as np

NOTES_NAME = ["A", "A#", "B", "C", "C#", "D",
              "D#", "E", "F", "F#", "G", "G#"]
NOTES_DICT = {"A": 0, "A#": 1, "B": 2, "C": 3, "C#": 4, "D": 5,
              "D#": 6, "E": 7, "F": 8, "F#": 9, "G": 10, "G#": 11}
LOWEST_NOTE = 27.50
RESTING_FREQUENCY = 60

SOPRANO = ["C4", "A5"]
MEZZO_SOPRANO = ["A3", "F5"]
ALTO = ["G3", "E4"]
TENOR = ["C3", "A4"]
BARITONE = ["A2", "F4"]
BASS = ["F2", "E4"]
VOCAL_RANGES = [BASS, BARITONE, TENOR, ALTO, MEZZO_SOPRANO, SOPRANO]
VOCAL_RANGES_VAL = [[87.30705785825097, 329.62755691287],
                    [55.0, 349.2282314330039],
                    [130.8127826502993, 220.0],
                    [195.99771799087466, 329.62755691287],
                    [110.0, 698.4564628660079],
                    [261.6255653005986, 440.0]]
VOCAL_RANGES_NAME = ['BASS', 'BARITONE', 'TENOR', 'ALTO', 'MEZZO_SOPRANO', 'SOPRANO']


class Music_note():
    def __init__(self, t_start, t_end, frequency=None, note=None):
        if note is None and frequency is None:
            raise Exception("you must enter either note or frequency")
        elif note is None:
            if frequency < 27.50:
                self.note = "N/A"
                self.frequency = 27.50
            else:
                number = int(math.log2(frequency / LOWEST_NOTE) * 12)
                octive = math.floor(number / 12)
                note_id = number % 12
                self.frequency = LOWEST_NOTE * pow(2, number / 12.0)
                self.note = NOTES_NAME[note_id] + "{}".format(octive + 1)
        else:
            try:
                octive = int(note[-1]) - 1
                note_id = NOTES_DICT[note[:-1]]
                self.frequency = LOWEST_NOTE * pow(2, (octive * 12 + note_id) / 12.0)
                self.note = note
            except:
                self.note = "N/A"
                self.frequency = 0
        self.t_start = t_start
        self.t_end = t_end
        self.duration = t_end - t_start

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

    @staticmethod
    def freq2note(frequency):
        if frequency < 27.50:
            return "N/A"
        else:
            number = int(math.log2(frequency / LOWEST_NOTE) * 12)
            octive = math.floor(number / 12)
            note_id = number % 12
            return NOTES_NAME[note_id] + "{}".format(octive + 1)

    @staticmethod
    def note2freq(note):
        try:
            octive = int(note[-1]) - 1
            note_id = NOTES_DICT[note[:-1]]
            frequency = LOWEST_NOTE * pow(2, (octive * 12 + note_id) / 12.0)
            return frequency
        except:
            return 0

    def play(self):
        if self.note == "N/A":
            time.sleep(self.duration)
        else:
            winsound.Beep(int(self.frequency), int(self.duration * 1000))

class PraatScriptWrapper():
    def __init__(self, audio_path_file, pitch_ceiling = 1000):
        # the audio file should be 44.1kHz for accurate pitch prediction result.
        # the audio file could be a mp3 file
        self.pitch_ceiling = pitch_ceiling
        self.dt = 0.01
        self.snd = parselmouth.Sound(audio_path_file)
        self.pitch = self.snd.to_pitch(time_step = self.dt, pitch_ceiling = self.pitch_ceiling)

        # pre-init variable used for storing vibrato information
        self.vibrato_intervals = []

        # list for storing phoneme and word_alignment info
        self.phoneme_list = []
        self.phoneme_onsets = []
        self.word_list = []
        self.word_intervals = []

    def compute_self_vibrato(self):
        if len(self.vibrato_intervals) == 0:
            strength = self.pitch.selected_array["strength"]
            frequency = self.pitch.selected_array["frequency"]
            frequency[strength < 0.5] = 0
            frequency[frequency == 0] = np.nan
            frequency_xs = self.pitch.xs()
            self.vibrato_intervals = self.compute_vibrato(frequency, frequency_xs, self.dt)
        return self.vibrato_intervals
    def compute_vibrato(self, frequency, frequency_xs, dt):

        # this function computes vibrato by analyzing the zero-crossing of the input frequency array
        # if it can identify 3 zero crossing that are equally spaced apart, then it recognize those
        # as a vibrato.

        min_zero_crossing_distance = 1.0 / 14  # max vibrato frequency = 7 Hz = 14 zero crossings per second
        self.tolerance = dt * 2.5  # using the uncertainty of the instrument (pitch measuring device) to bound tolerance

        # compute time derivative
        d_frequency_dt = correlate(frequency, np.array([-1.0, 0, 1.0]), mode="same") / dt / 2

        # obtain zero crossings
        zero_crossing = []
        for i in range(0, d_frequency_dt.shape[0] - 1):
            if (d_frequency_dt[i] < 0 and d_frequency_dt[i + 1] >= 0) or (
                    d_frequency_dt[i] > 0 and d_frequency_dt[i + 1] <= 0):
                zero_crossing.append(i + 1)

        # choose sets of zero crossing and identify vibratos within those
        distance = 0
        in_vibrato = 0
        starting_time = -1
        vibrato_intervals = []
        for i in range(0, len(zero_crossing) - 1):
            current_distance = frequency_xs[zero_crossing[i + 1]] - frequency_xs[zero_crossing[i]]

            if abs(current_distance - distance) <= self.tolerance and current_distance >= min_zero_crossing_distance:
                if in_vibrato == 0:
                    starting_time = zero_crossing[i - 1]
                    distance = (distance + current_distance) / 2  # calculate new average
                    in_vibrato = 1
                elif in_vibrato > 0:
                    distance = (distance * in_vibrato + current_distance) / (in_vibrato + 1)  # calculate new average
                    in_vibrato = in_vibrato + 1
            else:
                if in_vibrato > 0:
                    distance = current_distance
                    if in_vibrato > 2:
                        vibrato_intervals.append([frequency_xs[starting_time], frequency_xs[zero_crossing[i]]])
                    in_vibrato = 0
                else:
                    distance = current_distance
        return vibrato_intervals
    def write_praat_script(self, output_path, file_name):
        new_grid = textgrids.TextGrid()  # initialize new_textgrid object
        new_grid.xmin = 0
        new_grid.xmax = self.pitch.xs()[-1]
        if len(self.phoneme_list) > 0:
            new_grid["phones"] = []
            for i in range(1, len(self.phoneme_onsets) - 1):
                phoneme = self.phoneme_list[i]
                if phoneme == ">":
                    phoneme = ""
                interval = textgrids.Interval(phoneme, self.phoneme_onsets[i], self.phoneme_onsets[i + 1])
                new_grid["phones"].append(interval)
        if len(self.word_list) > 0:
            new_grid["words"] = []
            for i in range(0, len(self.word_list)):
                interval = textgrids.Interval(self.word_list[i], self.word_durations[i][0], self.word_durations[i][1])
                new_grid["words"].append(interval)
        if len(self.vibrato_intervals) > 0:
            new_grid["vibrato"] = []
            for i in range(0, len(self.vibrato_intervals)):
                interval = textgrids.Interval("vibrato", self.vibrato_intervals[i][0], self.vibrato_intervals[i][1])
                new_grid["vibrato"].append(interval)
        new_grid.write(os.path.join(output_path, file_name) + ".TextGrid")

def format_conversion_m4a2wav(file_name: str):
    filename = './Jali_Experiments/Jali_Experiments.{}'
    from pydub import AudioSegment
    audio: pydub.audio_segment.AudioSegment = AudioSegment.from_file(filename.format("wav"))
    audio.export(filename.format("wav"), format="s16be")
    os.remove(filename.format("m4a"))
    return 0

if __name__ == "__main__":
    pw = PraatScriptWrapper("E:/ten_videos/Child_in_time/Child_in_time_2/audio.mp3")
    pw.compute_self_vibrato()
    pw.write_praat_script("E:/ten_videos/Child_in_time/Child_in_time_2/", "vibrato")



