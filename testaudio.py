import pytest
import numpy as np
from welcome import extract_mfcc_features

# Define a test case for the extract_mfcc_features function
def test_extract_mfcc_features():
    # Define a sample audio file path
    audio_file = "c:/Users/bishm/Downloads/testaudio.wav"
    
    # Call the extract_mfcc_features function
    features = extract_mfcc_features(audio_file)
    
    # Check if the features have the expected shape
    assert features.shape == (26,)  # Assuming 13 MFCCs with mean and standard deviation
