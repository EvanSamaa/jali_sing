import json as json
import os

class MusicScript():
    def __init__(self, phoneme_list, phoneme_onset):
        length = len(phoneme_list)
        self.onset = phoneme_onset
        self.phonemes = phoneme_list
        self.t = 0
        self.current_index = 0
    def update(self, dt):
        self.t = self.t + dt
        pass
    def get_current_phoneme(self):

    def get_next_phoneme(self):
        pass
    def get_prev_phoneme(self):
        pass
    def get_phoneme_dt_away(self):
        pass