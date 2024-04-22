import streamlit as st
import os
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf


from tensorflow.keras.models import load_model

# Function to extract MFCC features from an audio file
def extract_mfcc_features(audio_file, num_mfcc=13):
    y, sr = librosa.load(audio_file, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=num_mfcc)
    mfccs_mean = np.mean(mfccs, axis=1)
    mfccs_std = np.std(mfccs, axis=1)
    return np.concatenate((mfccs_mean, mfccs_std))

# Load the trained model
model = load_model('cnn_model.h5')

# Load the scaler fitted during training
scaler = StandardScaler()
scaler.fit(X_train)  # Assuming X_train is the standardized training data

# Streamlit app
st.title("German Pronunciation Prediction")

# File uploader for uploading audio files
uploaded_file = st.file_uploader("Upload an audio file", type=["wav"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with open("temp.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract MFCC features from the uploaded audio file
    features = extract_mfcc_features("temp.wav")
    
    # Standardize the features using the scaler fitted during training
    scaled_features = scaler.transform(features.reshape(1, -1))
    
    # Use the trained model to predict the pronunciation accuracy
    prediction_prob = model.predict(scaled_features)[0][0]
    
    # Define the thresholds for different categories
    incorrect_threshold = 0.4
    partly_correct_threshold = 0.9
    
    # Check the predicted probability and assign marks accordingly
    if prediction_prob <= incorrect_threshold:
        score = prediction_prob * 40  # Marks less than 40 for incorrect pronunciation
        feedback = "The pronunciation is incorrect."
    elif prediction_prob <= partly_correct_threshold:
        score = 40 + (prediction_prob - incorrect_threshold) / (partly_correct_threshold - incorrect_threshold) * 50  # Marks between 40 and 90 for partly correct pronunciation
        feedback = "The pronunciation is partly correct."
    else:
        score = 90 + (prediction_prob - partly_correct_threshold) / (1 - partly_correct_threshold) * 10  # Marks between 90 and 100 for excellent pronunciation
        feedback = "The pronunciation is excellent."
    
    # Output the score and feedback
    st.write("Pronunciation Score: {:.2f}/100".format(score))
    st.write("Feedback: {}".format(feedback))
