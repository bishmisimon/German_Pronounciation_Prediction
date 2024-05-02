import os
import librosa
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler
import torch.nn as nn
import io
import streamlit as st

# Define the ANN model using PyTorch
class ANNModel(nn.Module):
    def __init__(self, input_size):
        super(ANNModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        return self.sigmoid(x)

# Load the PyTorch model
torch_ann_model = torch.load("modelcnn.pth")

# Main Streamlit app
st.title("Pronunciation Accuracy Prediction")

# File uploader for multiple files
uploaded_files = st.file_uploader("Upload one or more audio files", accept_multiple_files=True, type=["wav"])

if uploaded_files:
    # Display audio players for each uploaded file
    for uploaded_file in uploaded_files:
        st.audio(uploaded_file, format='audio/wav')

        # Extract features
        y, sr = librosa.load(io.BytesIO(uploaded_file.read()), sr=None)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfccs_mean = np.mean(mfccs, axis=1)
        mfccs_std = np.std(mfccs, axis=1)
        features = np.concatenate((mfccs_mean, mfccs_std))

        # Standardize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features.reshape(1, -1))

        # Convert numpy array to PyTorch tensor
        features_tensor = torch.tensor(features_scaled, dtype=torch.float32)

        # Make prediction using the PyTorch model
        output = torch_ann_model(features_tensor)
        prediction = torch.round(output).item()

        # Score pronunciation level
        pronunciation_score = output.item() * 100  # Multiplying by 100 to get a score out of 100

        # Provide feedback to the speaker based on pronunciation score and prediction
        feedback = "Your pronunciation is excellent!" if prediction == 1 else "Your pronunciation needs improvement."

        # Display results in a table
        st.write("Audio File:", uploaded_file.name)
        st.write("Pronunciation Score (out of 100):", round(pronunciation_score, 2))
        st.write("Model Prediction:", "Correct" if prediction == 1 else "Incorrect")
        st.write("Feedback:", feedback)
