import parselmouth
import pickle
import os
import numpy as np
# from scipy.signal import decimate
import torch
import json
from plla_tisvs.preprocessing_input import Custom_data_set
import plla_tisvs.testx as testx
from plla_tisvs.estimate_alignment import optimal_alignment_path, compute_phoneme_onsets
import librosa
from scipy.io import wavfile
import textgrids

def compute_word_alignment(phoneme_onsets, phoneme_list_full):
    word_durations = []
    pointer_i = 0 # this one is for the phoneme_list_full
    pointer_j = 0 # this one is for phoneme_onsets
    begin = phoneme_onsets[pointer_j]
    phone_copy = ['EOW'] + phoneme_list_full
    while pointer_j < len(phoneme_onsets):
        if phone_copy[pointer_i] == "EOW":
            word_durations.append([begin, phoneme_onsets[pointer_j]])
            if pointer_j + 1 == len(phoneme_onsets):
                break
            if phoneme_onsets[min(pointer_j + 1, len(phoneme_onsets)-1)] != "<":
                begin = phoneme_onsets[min(pointer_j + 1, len(phoneme_onsets)-1)]
                pointer_i = pointer_i + 2
                pointer_j = pointer_j + 1
            else:
                begin = phoneme_onsets[min(pointer_j + 2, len(phoneme_onsets)-1)]
                pointer_i = pointer_i + 3
                pointer_j = pointer_j + 2
        else:
            pointer_i = pointer_i + 1
            pointer_j = pointer_j + 1
    return word_durations[1:]

if __name__ == "__main__":

    dict_path = "./plla_tisvs/dicts"
    model_path = './plla_tisvs/trained_models/{}'.format("JOINT3")
    phoneme_dict_path = "cmu_word2cmu_phoneme_extra.pickle"
    audio_paths = ["E:/ten_videos/Child_in_time/Child_in_time_2/audio.wav"]
    transcript_paths = ["E:/ten_videos/Child_in_time/Child_in_time_2/audio.txt"]
    output_path = "E:/ten_videos/Child_in_time/Child_in_time_2"

    # parse data
    data_parser = Custom_data_set(dict_path, phoneme_dict_path)
    audio, phoneme_idx, phoneme_list_full, word_list = data_parser.parse(audio_paths[0], transcript_paths[0])

    # load model
    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
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
    phoneme_list = data_parser.get_phonemes(phoneme_idx[0])
    word_durations = compute_word_alignment(phoneme_onsets, phoneme_list_full)
    for i in range(1, len(phoneme_onsets) - 1):
        print(phoneme_list[i], '\t', phoneme_onsets[i], phoneme_onsets[i + 1])

    new_grid = textgrids.TextGrid()  # initialize new_textgrid object

    new_grid.xmin = 0
    new_grid.xmax = phoneme_onsets[-1]
    new_grid["phones"] = []
    for i in range(1, len(phoneme_onsets) - 1):
        phoneme = phoneme_list[i]
        if phoneme == ">":
            phoneme = ""
        interval = textgrids.Interval(phoneme, phoneme_onsets[i], phoneme_onsets[i + 1])
        new_grid["phones"].append(interval)

    new_grid["words"] = []
    for i in range(0, len(word_list)):
        interval = textgrids.Interval(word_list[i], word_durations[i][0], word_durations[i][1])
        new_grid["words"].append(interval)
    new_grid.write(output_path + "/alignment_from_killian.TextGrid")
