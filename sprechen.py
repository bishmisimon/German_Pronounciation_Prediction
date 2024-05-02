import streamlit as st
import numpy as np
import pickle
import pyaudio
import wave
import librosa
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from threading import Thread
import time
import os

# Function to extract prosodic features from audio data
def extract_prosodic_features(audio_data, sample_rate):
    pitch = librosa.yin(audio_data, fmin=50, fmax=2000)
    energy = librosa.feature.rms(y=audio_data)
    duration = librosa.get_duration(y=audio_data, sr=sample_rate)
    pitch_mean = np.mean(pitch)
    pitch_std = np.std(pitch)
    energy_mean = np.mean(energy)
    energy_std = np.std(energy)
    features = {
        'pitch_mean': pitch_mean,
        'pitch_std': pitch_std,
        'energy_mean': energy_mean,
        'energy_std': energy_std,
        'duration': duration
    }
    return features

# Function to record audio from microphone
def record_audio(file_path, duration=5, chunk_size=1024, sample_format=pyaudio.paInt16, channels=1, sample_rate=44100):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=sample_format,
                        channels=channels,
                        rate=sample_rate,
                        frames_per_buffer=chunk_size,
                        input=True)
    frames = []
    start_time = time.time()
    while time.time() - start_time < duration:
        data = stream.read(chunk_size)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(sample_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

# Function to predict pronunciation based on prosodic features
def predict_pronunciation(features):
    # Load the trained SVM model
    with open('svm_model.pkl', 'rb') as f:
        model_svm = pickle.load(f)

    # Load the scaler object
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # Scale features
    X = np.array([list(features.values())])
    X_scaled = scaler.transform(X)

    # Predict pronunciation
    prediction = model_svm.predict(X_scaled)

    return 'correct' if prediction == 1 else 'incorrect'

st.title('German Pronunciation Prediction')

# Record voice input
if st.button('Record Voice'):
    st.session_state.stop_recording = False  # Initialize session state variable
    st.write('Recording...')
    # Generate a new audio file path for each recording
    audio_file_path = f"recorded_audio_{int(time.time())}.wav"
    record_audio(audio_file_path)
    # Display the recorded audio
    st.audio(audio_file_path, format='audio/wav')
    # Extract prosodic features from the recorded voice
    audio_data, sample_rate = librosa.load(audio_file_path, sr=None)
    features = extract_prosodic_features(audio_data, sample_rate)
    print("Features:", features)  # Add print statement to check features
    # Predict pronunciation
    prediction = predict_pronunciation(features)
    st.write(f'Prediction: {prediction}')
