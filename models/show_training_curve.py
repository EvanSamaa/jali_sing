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
from vowel_recognition_nodel import LSTM_vowel_recognizer, Custom_Dataset, build_confusion_matrix, accuracy

if __name__ == "__main__":
    if torch.cuda.is_available():
        dev = "cuda:1"
        torch.set_default_tensor_type('torch.cuda.FloatTensor')
    else:
        dev = "cpu"


    dataset_root = "../../Dataset/"
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
    model_name = "viseme_net_model_larger_model/"
    model_loc = dataset_root + model_name
    model_names = os.listdir(model_loc)

    testing_set = Custom_Dataset(os.path.join(dataset_root, os.path.join("test", 'annotations_medusa.csv')), None)
    test_dataloader = DataLoader(testing_set, batch_size=512, shuffle=False)
    loss_fn = torch.nn.CrossEntropyLoss()

    confusion_matrices = []
    train_loss = []
    test_loss = []
    test_accuracy = []

    for m in model_names:
        model_path = model_loc + m
        model = LSTM_vowel_recognizer()
        time = int(m.split("_")[-1][:-3])
        state_dict = torch.load(model_path)
        model.load_state_dict(state_dict['model_state_dict'])
        model.eval()
        mean_accuracy = 0
        weight = 1
        mean_confusion_matrix = np.zeros((6, 6))
        for sentence, tags in test_dataloader:
            with torch.no_grad():
                vowel_prediction = model(sentence)
                vowel_prediction_flat = vowel_prediction.view(
                    [vowel_prediction.shape[0] * vowel_prediction.shape[1], -1])
                target_flat = tags.view([tags.shape[0] * tags.shape[1], ])
                # Step 4. Compute the loss, gradients, and update the parameters by
                loss = loss_fn(vowel_prediction_flat, target_flat)
                acc_val = accuracy(vowel_prediction_flat, target_flat).cpu().numpy()
                mean_accuracy = mean_accuracy + acc_val * tags.shape[0] * tags.shape[1]
                weight = weight + tags.shape[0] * tags.shape[1]
                mean_confusion_matrix = build_confusion_matrix(vowel_prediction_flat, target_flat, mean_confusion_matrix)
                break
        test_accuracy.append([time, mean_accuracy/(weight-1)])
        confusion_matrices.append([time, confusion_matrices])
        if len(test_accuracy) == 2:
            test_accuracy = sorted(test_accuracy, key=lambda x: x[0])
            confusion_matrices = sorted(confusion_matrices, key=lambda x: x[0])
            print(test_accuracy)
            print(confusion_matrices)