import os
import streamlit as st
import librosa
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler

# Function to extract MFCC features from an audio file
def extract_mfcc_features(audio_file, num_mfcc=13):
    y, sr = librosa.load(audio_file, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=num_mfcc)
    mfccs_mean = np.mean(mfccs, axis=1)
    mfccs_std = np.std(mfccs, axis=1)
    return np.concatenate((mfccs_mean, mfccs_std))

# Function to provide feedback based on pronunciation score
def provide_feedback(pronunciation_score):
    if pronunciation_score >= 80:
        return "Your pronunciation is excellent!"
    elif 60 < pronunciation_score < 80:
        return "Your pronunciation is good, but there's room for improvement."
    elif 40 <= pronunciation_score <= 60:
        return "Your pronunciation needs improvement."
    else:
        return "Your pronunciation needs significant improvement. Consider seeking assistance."

# Load the PyTorch model
torch_ann_model = torch.load("modelcnn.pth")

# Main Streamlit app
st.title("Pronunciation Accuracy Prediction")

# File uploader
uploaded_file = st.file_uploader("Upload an audio file", type=["wav"])

if uploaded_file is not None:
    # Extract features
    features = extract_mfcc_features(uploaded_file)
    
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
    feedback = provide_feedback(pronunciation_score)

    # Display results
    st.write("Pronunciation Score (out of 100):", round(pronunciation_score, 2))
    st.write("Model Prediction:", "Correct" if prediction == 1 else "Incorrect")
    st.write("Feedback:", feedback)
