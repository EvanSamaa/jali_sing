import torch.nn as nn
import torch
import torch.nn.functional as F
import torch.optim as optim
import os
import numpy as np
from collections import OrderedDict
import pandas as pd
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from .vowel_recognition_nodel import LSTM_vowel_recognizer

if __name__ == "__main__":
    dataset_root = "../../Dataset/"
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
    model_name = "viseme_net_model_larger_model"
    model_loc = dataset_root + model_name
    model_names = os.listdir(model_loc)

    confusion_matrices = []
    accuracy = []
    loss = []

    for m in model_names:
        model_path = model_loc + m
        print(model_path)

