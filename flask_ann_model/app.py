import os
import numpy as np
import pickle
import requests
from flask import Flask, request, jsonify
import pyaudio
import wave
import librosa

# Load the trained SVM model
with open('svm_model.pkl', 'rb') as f:
    model_svm = pickle.load(f)

# Load the scaler object
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

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
    for _ in range(0, int(sample_rate / chunk_size * duration)):
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

app = Flask(__name__)

# Route to predict pronunciation
@app.route('/predict', methods=['POST'])
def predict():
    if 'record' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400
    
    # Record audio from the microphone
    audio_file_path = "recorded_audio.wav"
    record_audio(audio_file_path)
    
    # Load the recorded audio data
    audio_data, sample_rate = librosa.load(audio_file_path, sr=None)
    
    # Extract prosodic features
    features = extract_prosodic_features(audio_data, sample_rate)
    
    # Scale features
    X = np.array([list(features.values())])
    X_scaled = scaler.transform(X)
    
    # Predict pronunciation
    prediction = model_svm.predict(X_scaled)
    
    # Return prediction result
    return jsonify({'prediction': 'correct' if prediction == 1 else 'incorrect'}), 200

if __name__ == '__main__':
    app.run(debug=True)
