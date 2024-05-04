import unittest
from welcome import extract_mfcc_features
import numpy as np


class TestExtractMFCCFeatures(unittest.TestCase):
    def test_extract_mfcc_features(self):
        # Define an audio file path for testing
        audio_file = "testaudio.wav"  # Replace with your test audio file path
        
        # Call the extract_mfcc_features function
        features = extract_mfcc_features(audio_file)
        
        # Assertions
        self.assertIsNotNone(features)  # Ensure features are not None
        self.assertIsInstance(features, np.ndarray)  # Ensure features are numpy array
        self.assertEqual(features.shape[0], 26)  # Ensure correct number of features extracted (13 mean + 13 std)

if __name__ == "__main__":
    unittest.main()
