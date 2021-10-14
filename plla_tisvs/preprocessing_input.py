import parselmouth
import pickle
import os
import numpy as np
from scipy.signal import decimate
import torch
import json
from .estimate_alignment import optimal_alignment_path, compute_phoneme_onsets
from . import testx

class Custom_data_set():
    def __init__(self, dict_path, phoneme_dict_path):
        cmu_vocabulary = ['#', '$', '%', '>', '-', 'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', 'EH', 'ER',
                      'EY', 'F', 'G',
                      'HH', 'IH', 'IY', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH', 'T', 'TH',
                      'UH',
                      'UW', 'V', 'W', 'Y', 'Z', 'ZH']
        self.cmu_phoneme2idx = {}
        self.cmu_idx2phoneme = {}
        for idx, phoneme in enumerate(cmu_vocabulary):
            self.cmu_phoneme2idx[phoneme] = idx
            self.cmu_idx2phoneme[idx] = phoneme
        with open(os.path.join(dict_path, phoneme_dict_path), "rb") as file:
            self.word2phoneme_dict = pickle.load(file)
        with open(os.path.join(dict_path, "cmu_symbols2phones.pickle"), "rb") as file:
            self.symbol2phoneme_dict = pickle.load(file)

    def parse(self, audio_path, transcirpt_path):
        phoneme_list = []

        # load the transcript file
        with open(transcirpt_path, "r") as file:
            transcript = file.read()

        # replace useless symbols
        transcript = transcript.replace("\n", " ")
        transcript = transcript.replace(",", "")
        transcript = transcript.replace(".", "")

        for word in transcript.split():
            phonemes = self.word2phoneme_dict[word.lower()]
            for phoneme in phonemes.split():
                phoneme_list.append(self.symbol2phoneme_dict[phoneme])
                phoneme_list.append(">")
        phoneme_list = phoneme_list[:-1]
        phoneme_idx = np.array([self.cmu_phoneme2idx[p] for p in phoneme_list])
        phoneme_idx = np.pad(phoneme_idx, (1, 1), mode='constant', constant_values=1)
        phoneme_idx_torch = torch.from_numpy(phoneme_idx)

        # load the audio file into a readable format for the model
        sound_object = parselmouth.Sound(audio_path)
        sound = sound_object.values
        fps = sound_object.sampling_frequency
        sound = decimate(sound, int(fps / 16000))
        print(sound.shape)
        sound_torch = torch.from_numpy(sound.copy()).type(torch.float32)

        sound_torch_out = sound_torch.unsqueeze(dim=0)
        phoneme_idx_out = phoneme_idx_torch.unsqueeze(dim=0)
        return sound_torch_out, phoneme_idx_out
    def get_phonemes(self, idx_list):
        # input should be an 1D array of indexes, it will be turned into a list of phonemes
        out = []
        for i in range(0, idx_list.size()[0]):
            out.append(self.cmu_idx2phoneme[int(idx_list[i].item())])
        return out
if __name__ == "__main__":
    dict_path = "./dicts"
    phoneme_dict_path = "cmu_word2cmu_phoneme_extra.pickle"
    audio_paths = ["/Volumes/EVAN_DISK/ten_videos/Child_in_time/Child_in_time_1/audio.wav"]
    transcript_paths = ["/Volumes/EVAN_DISK/ten_videos/Child_in_time/Child_in_time_1/audio.txt"]

    data_parser = Custom_data_set(dict_path, phoneme_dict_path)
    audio, phoneme_idx = data_parser.parse(audio_paths[0], transcript_paths[0])

    # load model

    model_path = 'trained_models/{}'.format("JOINT3")
    #device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    device = 'cpu'
    print("Device:", device)
    target = 'vocals'

    # load model
    model_to_test = testx.load_model(target, model_path, device)
    model_to_test.return_alphas = True
    model_to_test.eval()

    # load model config
    with open(os.path.join(model_path, target + '.json'), 'r') as stream:
        config = json.load(stream)
        samplerate = config['args']['samplerate']
        text_units = config['args']['text_units']
        nfft = config['args']['nfft']
        nhop = config['args']['nhop']

    with torch.no_grad():
        vocals_estimate, alphas, scores = model_to_test((audio, phoneme_idx))

    optimal_path_scores = optimal_alignment_path(scores, mode='max_numpy', init=200)

    phoneme_onsets = compute_phoneme_onsets(optimal_path_scores, hop_length=nhop, sampling_rate=samplerate)
    print(len(phoneme_onsets))
    print()



