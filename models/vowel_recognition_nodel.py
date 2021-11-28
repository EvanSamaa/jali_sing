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

class Custom_Dataset(Dataset):
    def __init__(self, annotations_file, device):
        self.img_labels = pd.read_csv(annotations_file)
    def __len__(self):
        return len(self.img_labels)
    def __getitem__(self, idx):
        data_path = self.img_labels.iloc[idx, 0]
        data = torch.tensor(np.load(data_path), dtype=torch.float32)
        label_path = self.img_labels.iloc[idx, 1]
        label = torch.tensor(np.load(label_path), dtype=torch.long)
        return data, label

# this is the one I used
class LSTM_vowel_recognizer(nn.Module):
    def __init__(self, hidden_dim=256, win_length=12, num_lstm_layer=3):
        super(LSTM_vowel_recognizer, self).__init__()
        # here I'm going to assume the input is gonna be shaped as
        self.hidden_dim = hidden_dim
        self.win_length = win_length
        self.num_lstm_layer = num_lstm_layer
        # The LSTM takes word embeddings as inputs, and outputs hidden states
        # with dimensionality hidden_dim.
        self.lstm = nn.LSTM(65 * (self.win_length * 2 + 1), self.hidden_dim, num_lstm_layer)
        self.output_mat1 = nn.Linear(self.hidden_dim, 6)
        self.output_mat2 = nn.Linear(64, 64)
        self.output_mat3 = nn.Linear(64, 6)
        self.relu = nn.ReLU()
        self.bn = nn.BatchNorm1d(self.hidden_dim)
        self.bn1 = nn.BatchNorm1d(64)
        self.bn2 = nn.BatchNorm1d(64)

        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax()
    def concate_frames(self, input_audio):
        padding = torch.zeros((input_audio.shape[0], self.win_length, input_audio.shape[2]))
        padded_input_audio = torch.cat([padding, input_audio, padding], dim=1)
        window_audio = []
        for i in range(0, input_audio.shape[1]):
            window_count = i + 12
            current_window = padded_input_audio[:, window_count-12:window_count+13]
            s = current_window.shape
            current_window = current_window.view((s[0], s[1] * s[2]))
            current_window = torch.unsqueeze(current_window, 1)
            window_audio.append(current_window)
        rtv = torch.cat(window_audio, dim=1)
        return rtv

    def forward(self, input_audio):
        mod_audio = self.concate_frames(input_audio)
        # here I'm assuming that the input_audio is of shape
        hidden_state = [torch.zeros((self.num_lstm_layer, mod_audio.shape[1], self.hidden_dim)), torch.zeros((self.num_lstm_layer, mod_audio.shape[1], self.hidden_dim))]
        out, hidden_state = self.lstm(mod_audio, hidden_state)
        # bn
        x = self.bn(out.permute(0, 2, 1)).permute(0, 2, 1)
        x = self.relu(x)
        x = self.output_mat1(x)
        return x

    def test_forward(self, input_audio):
        x = self.forward(input_audio)
        return self.softmax(x)
def accuracy(output, label):
    maxy = torch.argmax(output, dim=1)
    correct = torch.where(maxy == label, 1, 0)
    accuracy = correct.sum()/correct.shape[0]
    return accuracy

def build_confusion_matrix(output, label, mat):
    out = mat
    maxy = torch.argmax(output, dim=1)
    for i in range(0, output.shape[0]):
        out[maxy[i], label[i]] = out[maxy[i], label[i]] + 1
    return out

if __name__ == "__main__":

    # input things
    # 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
    dataset_root = "C:/Users/evansamaa/Desktop/Dataset/"
    model_name = "viseme_net_model_smaller_lr"
    # prepare pytorch stuff
    if torch.cuda.is_available():
        dev = "cuda:1"
        dataset_root = "../../Dataset/"
        torch.set_default_tensor_type('torch.cuda.FloatTensor')
    else:
        dev = "cpu"
    print("running on {}".format(dev))
    device = torch.device(dev)
    try:
        os.mkdir(os.path.join(dataset_root, model_name))
    except:
        print("overwriting old directory of {}".format(model_name))
    torch.manual_seed(0)

    model = LSTM_vowel_recognizer()
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.00001)
    epochs = 10000
    training_set = Custom_Dataset(os.path.join(dataset_root, os.path.join("train", 'annotations_medusa.csv')), device)
    train_dataloader = DataLoader(training_set, batch_size=512, shuffle=False)
    testing_set = Custom_Dataset(os.path.join(dataset_root, os.path.join("test", 'annotations_medusa.csv')), device)
    test_dataloader = DataLoader(testing_set, batch_size=512, shuffle=False)
    checkpoint_path = os.path.join(dataset_root, model_name+"/model_epoch_{}.pt")
    test_sent = 0
    test_tag = 0
    for sentence, tags in test_dataloader:
        test_sent = sentence
        test_tag = tags
        break

    loss_this_epoch = []
    loss_prev_epoch = [20]

    for epoch in range(epochs):  # again, normally you would NOT do 300 epochs, it is toy data
        for sentence, tags in train_dataloader:
            # Step 1. Remember that Pytorch accumulates gradients.
            # We need to clear them out before each instance
            model.zero_grad()
            vowel_prediction = model(sentence)
            vowel_prediction_flat = vowel_prediction.view([vowel_prediction.shape[0] * vowel_prediction.shape[1], -1])
            target_flat = tags.view([tags.shape[0] * tags.shape[1], ])
            # Step 4. Compute the loss, gradients, and update the parameters by
            loss = loss_fn(vowel_prediction_flat, target_flat)
            loss.backward()
            optimizer.step()
            loss_val = loss.data.cpu().numpy()
            acc_val = accuracy(vowel_prediction_flat, target_flat).cpu().numpy()
            print("epoch = ", epoch, "\t\t", "loss = ", loss_val, "\t\t", "accuracy = ", acc_val)
            loss_this_epoch.append(loss_val)

        if epoch%20 == 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': loss,
            }, checkpoint_path.format(epoch))

            with torch.no_grad():
                vowel_prediction = model(test_sent)
                vowel_prediction_flat = vowel_prediction.view(
                    [vowel_prediction.shape[0] * vowel_prediction.shape[1], -1])
                target_flat = test_tag.view([test_tag.shape[0] * test_tag.shape[1], ])
                # Step 4. Compute the loss, gradients, and update the parameters by
                acc_val = accuracy(vowel_prediction_flat, target_flat).cpu().numpy()
                print(acc_val)
            prev = np.array(loss_prev_epoch).mean()
            curr = np.array(loss_this_epoch).mean()
            if prev - curr < 0 or abs(prev - curr) < 0.00001 and epoch > 500:
                break
            else:
                loss_prev_epoch = loss_this_epoch
                loss_this_epoch = []


    # See what the scores are after training



