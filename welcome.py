import streamlit as st
import os
from PIL import Image
import pandas as pd
from datetime import datetime
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
import sounddevice as sd
import soundfile as sf

# Create a folder if it doesn't exist
os.makedirs("audios", exist_ok=True)

# Function to extract MFCC features from an audio file
def extract_mfcc_features(audio_file, num_mfcc=13):
    y, sr = librosa.load(audio_file, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=num_mfcc)
    mfccs_mean = np.mean(mfccs, axis=1)
    mfccs_std = np.std(mfccs, axis=1)
    return np.concatenate((mfccs_mean, mfccs_std))

# Load data and train the model
def load_data_and_train_model():
    # Define directories
    directory = 'All Audios'
    correct_directory = os.path.join(directory, 'Correct_Audio_dataset')
    incorrect_directory = os.path.join(directory, 'Incorrect_Audio_Dataset')

    # Extract MFCC features for correct pronunciations
    correct_features = []
    correct_labels = []
    for filename in os.listdir(correct_directory):
        if filename.endswith('.wav'):
            audio_file = os.path.join(correct_directory, filename)
            features = extract_mfcc_features(audio_file)
            correct_features.append(features)
            correct_labels.append(1)  # Use 1 for correct pronunciations

    # Extract MFCC features for incorrect pronunciations
    incorrect_features = []
    incorrect_labels = []
    for filename in os.listdir(incorrect_directory):
        if filename.endswith('.wav'):
            audio_file = os.path.join(incorrect_directory, filename)
            features = extract_mfcc_features(audio_file)
            incorrect_features.append(features)
            incorrect_labels.append(0)  # Use 0 for incorrect pronunciations

    # Combine features and labels
    X = np.vstack((correct_features, incorrect_features))
    y = np.hstack((correct_labels, incorrect_labels))

    # Split the data into train and test sets
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # Create and train the SVM model
    svm_model = make_pipeline(StandardScaler(), SVC(kernel='rbf', gamma='auto', probability=True))
    svm_model.fit(X_train_scaled, y_train)

    return svm_model, scaler

# Load the trained model and scaler
svm_model, scaler = load_data_and_train_model()

# Function to predict pronunciation accuracy
def predict_pronunciation_accuracy(audio_file_path):
    features = extract_mfcc_features(audio_file_path)
    scaled_features = scaler.transform(features.reshape(1, -1))
    prediction_prob = svm_model.predict_proba(scaled_features)[0][1]  # Probability of correct pronunciation
    return prediction_prob, audio_file_path  # Return the audio file path

# Main function to run the app
def main():
    logo_image = Image.open("Logo.png")
    # Display logo at the top of the page
    st.image(logo_image, use_column_width=True)

    # Title
    st.markdown(
        "<h1 style='text-align: center; color: #4169E1;'>Bewertung der deutschen Aussprache</h2>", 
        unsafe_allow_html=True
    )

    # Record or upload audio
    st.header("Record or Upload Audio")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Record Audio"):
            record_audio()

    with col2:
        uploaded_file = st.file_uploader("Upload Audio", type=["wav"])
        if uploaded_file is not None:
            st.audio(uploaded_file, format='audio/wav')
            if st.button("Evaluate Pronunciation - Upload", key="upload_btn"):
                evaluate_audio(uploaded_file)

    # Display saved audio files in a table
    audio_files = os.listdir("audios")
    if audio_files:
        st.header("Saved Audio Files")
        for selected_file in audio_files:
            audio_file_path = os.path.join("audios", selected_file)
            col1, col2 = st.columns([1, 1])
            with col1:
                st.audio(audio_file_path, format='audio/wav')
            with col2:
                if st.button(f"Evaluate Pronunciation - {selected_file}", key=f"saved_btn_{selected_file}"):
                    evaluate_audio(audio_file_path)
                if st.button(f"Delete {selected_file}", key=f"delete_btn_{selected_file}"):
                    os.remove(audio_file_path)
                    st.success(f"Audio file '{selected_file}' deleted successfully.")
                    st.experimental_rerun()

# Function to record audio
def record_audio():
    st.warning("Recording audio. Please speak into the microphone...")
    duration = 5  # Recording duration in seconds
    samplerate = 44100  # Sampling rate
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
    sd.wait()  # Wait for recording to complete
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    audio_file_path = os.path.join("audios", f"recorded_audio_{timestamp}.wav")
    # Check if the file already exists
    if os.path.exists(audio_file_path):
        st.warning("Audio file already exists.")
    else:
        sf.write(audio_file_path, audio_data, samplerate)
        st.success(f"Audio recorded and saved as {audio_file_path}")

# Function to evaluate audio
def evaluate_audio(audio_file):
    try:
        st.write("Evaluating audio...")
        prediction_prob, audio_path = predict_pronunciation_accuracy(audio_file)
        
        # Adjusting the score range
        pronunciation_score = (prediction_prob * 25) + 75  # Map probability to the range 75-100
        
        feedback = ""
        if pronunciation_score < 80:
            feedback = "The pronunciation needs improvement."
        elif pronunciation_score < 90:
            feedback = "The pronunciation is good."
        else:
            feedback = "The pronunciation is excellent."
        
        # Displaying the adjusted score
        st.write("Pronunciation Score: {:.2f}/100".format(pronunciation_score))
        st.write("Feedback: {}".format(feedback))

    except Exception as e:
        st.error(f"An error occurred during evaluation: {e}")

# Run the app
if __name__ == "__main__":
    main()