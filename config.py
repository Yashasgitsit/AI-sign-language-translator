"""
Configuration settings for the AI Sign Language Translator
"""

import os

# Camera settings
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
FPS = 30

# MediaPipe settings
MEDIAPIPE_CONFIDENCE = 0.5
MEDIAPIPE_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 2

# Model settings
MODEL_PATH = "models/sign_language_model.h5"
MODEL_INPUT_SIZE = (64, 64)
NUM_CLASSES = 26  # A-Z for ASL alphabet
SEQUENCE_LENGTH = 30  # Number of frames to consider for gesture recognition

# Training settings
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.2

# Data paths
DATA_DIR = "data"
TRAINING_DATA_DIR = os.path.join(DATA_DIR, "training")
TEST_DATA_DIR = os.path.join(DATA_DIR, "test")
MODELS_DIR = "models"

# Sign language classes (ASL alphabet)
ASL_CLASSES = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
]

# Display settings
WINDOW_NAME = "AI Sign Language Translator"
TEXT_COLOR = (0, 255, 0)  # Green
TEXT_FONT = 1
TEXT_SCALE = 1
TEXT_THICKNESS = 2

# Gesture recognition settings
GESTURE_THRESHOLD = 0.7  # Confidence threshold for gesture recognition
SMOOTHING_WINDOW = 5  # Number of frames for prediction smoothing

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TRAINING_DATA_DIR, exist_ok=True)
os.makedirs(TEST_DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
