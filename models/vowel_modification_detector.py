from .vowel_recognition_nodel import LSTM_vowel_recognizer_no_BN
import torch
import torch.nn as nn
import numpy as np
import python_speech_features as psf
import librosa
from matplotlib import pyplot as plt
class vowel_mod_detector():
    def __init__(self, model_dir = "./models/over_trained_model.pt"):
        if torch.cuda.is_available():
            dev = "cuda:1"
        else:
            dev = "cpu"
        self.model = LSTM_vowel_recognizer_no_BN()
        self.model.load_state_dict(torch.load(model_dir, map_location=torch.device(dev))["model_state_dict"])
    def __call__(self, sound_arr, *args, **kwargs):
        # audio should be the
        sound_arr = (sound_arr - sound_arr.mean()) / sound_arr.std()
        sr = 44100
        appended = False
        if sound_arr.shape[0] < sr * 0.2:
            sound_arr = np.concatenate([np.zeros((int(sr * 0.2), )), sound_arr], axis=0)
            appended = True
        winstep = 441
        mfcc_feat = psf.mfcc(sound_arr, samplerate=sr, winlen=0.02, nfft=2 * winstep, numcep=13)
        logfbank_feat = psf.logfbank(sound_arr, samplerate=sr, winlen=0.02, nfft=2 * winstep, nfilt=26)
        ssc_feat = psf.ssc(sound_arr, samplerate=sr, winlen=0.02, nfft=2 * winstep, nfilt=26)
        full_feat = np.concatenate([mfcc_feat, logfbank_feat, ssc_feat], axis=1)
        input_vec = torch.tensor(np.expand_dims(full_feat, axis=0), dtype=torch.float32)
        out_vec = self.model.test_forward(input_vec)[0]
        if appended:
            out = out_vec.detach().numpy()[20:]
        else:
            out = out_vec.detach().numpy()
        coarse_out = out[:, 0:4]
        coarse_out[:, 1] = out[:, 1] + out[:, 2]
        coarse_out[:, 2] = out[:, 3] + out[:, 4]
        coarse_out[:, 3] = out[:, 5]
        return out, coarse_out
