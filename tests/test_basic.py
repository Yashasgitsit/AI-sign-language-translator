"""
Basic tests for the AI Sign Language Translator
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sign_detector import SignDetector
from translator import SignTranslator
from utils import validate_landmarks, preprocess_image
import config

class TestSignDetector(unittest.TestCase):
    """Test cases for SignDetector class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = SignDetector()
    
    def test_detector_initialization(self):
        """Test if detector initializes correctly"""
        self.assertIsNotNone(self.detector.hands)
        self.assertIsNotNone(self.detector.mp_hands)
    
    def test_preprocess_landmarks(self):
        """Test landmark preprocessing"""
        # Create dummy landmarks (21 landmarks * 3 coordinates)
        dummy_landmarks = np.random.randn(63)
        
        processed = self.detector.preprocess_landmarks(dummy_landmarks)
        self.assertIsNotNone(processed)
        self.assertEqual(len(processed), 63)

class TestSignTranslator(unittest.TestCase):
    """Test cases for SignTranslator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.translator = SignTranslator()
    
    def test_translator_initialization(self):
        """Test if translator initializes correctly"""
        self.assertIsNotNone(self.translator.prediction_history)
        self.assertEqual(self.translator.current_prediction, "")
        self.assertEqual(self.translator.current_confidence, 0.0)
    
    def test_reset_functionality(self):
        """Test reset functionality"""
        # Add some dummy predictions
        self.translator.prediction_history.append(("A", 0.9))
        self.translator.current_prediction = "A"
        self.translator.current_confidence = 0.9
        
        # Reset
        self.translator.reset()
        
        # Check if reset worked
        self.assertEqual(len(self.translator.prediction_history), 0)
        self.assertEqual(self.translator.current_prediction, "")
        self.assertEqual(self.translator.current_confidence, 0.0)

class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_validate_landmarks(self):
        """Test landmark validation"""
        # Valid landmarks
        valid_landmarks = np.random.randn(63)
        self.assertTrue(validate_landmarks(valid_landmarks))
        
        # Invalid landmarks (wrong size)
        invalid_landmarks = np.random.randn(50)
        self.assertFalse(validate_landmarks(invalid_landmarks))
        
        # None landmarks
        self.assertFalse(validate_landmarks(None))
        
        # NaN landmarks
        nan_landmarks = np.full(63, np.nan)
        self.assertFalse(validate_landmarks(nan_landmarks))
    
    def test_preprocess_image(self):
        """Test image preprocessing"""
        # Create dummy image
        dummy_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        processed = preprocess_image(dummy_image, (64, 64))
        
        self.assertEqual(processed.shape, (64, 64, 3))
        self.assertTrue(np.all(processed >= 0.0))
        self.assertTrue(np.all(processed <= 1.0))

class TestConfig(unittest.TestCase):
    """Test cases for configuration"""
    
    def test_config_values(self):
        """Test if config values are reasonable"""
        self.assertGreater(config.CAMERA_WIDTH, 0)
        self.assertGreater(config.CAMERA_HEIGHT, 0)
        self.assertGreater(config.FPS, 0)
        self.assertEqual(len(config.ASL_CLASSES), 26)
        self.assertGreater(config.GESTURE_THRESHOLD, 0.0)
        self.assertLessEqual(config.GESTURE_THRESHOLD, 1.0)

if __name__ == '__main__':
    unittest.main()
