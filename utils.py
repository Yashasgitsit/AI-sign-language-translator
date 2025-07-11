"""
Utility functions for the AI Sign Language Translator
"""

import logging
import os
import cv2
import numpy as np
from typing import List, Tuple
import config

def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level
        
    Returns:
        Configured logger
    """
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('sign_translator.log')
        ]
    )
    
    return logging.getLogger(__name__)

def create_directories():
    """Create necessary directories for the project"""
    directories = [
        config.DATA_DIR,
        config.TRAINING_DATA_DIR,
        config.TEST_DATA_DIR,
        config.MODELS_DIR,
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory created/verified: {directory}")

def preprocess_image(image: np.ndarray, target_size: Tuple[int, int] = None) -> np.ndarray:
    """
    Preprocess image for model input
    
    Args:
        image: Input image
        target_size: Target size for resizing
        
    Returns:
        Preprocessed image
    """
    if target_size is None:
        target_size = config.MODEL_INPUT_SIZE
    
    # Resize image
    processed = cv2.resize(image, target_size)
    
    # Normalize pixel values
    processed = processed.astype(np.float32) / 255.0
    
    return processed

def calculate_hand_area(landmarks: np.ndarray) -> float:
    """
    Calculate the area of the hand based on landmarks
    
    Args:
        landmarks: Hand landmarks array
        
    Returns:
        Hand area
    """
    if landmarks is None or len(landmarks) < 63:
        return 0.0
    
    # Reshape landmarks to (21, 3)
    landmarks_reshaped = landmarks.reshape(21, 3)
    
    # Get x and y coordinates
    x_coords = landmarks_reshaped[:, 0]
    y_coords = landmarks_reshaped[:, 1]
    
    # Calculate bounding box area
    width = np.max(x_coords) - np.min(x_coords)
    height = np.max(y_coords) - np.min(y_coords)
    
    return width * height

def smooth_landmarks(landmarks_sequence: List[np.ndarray], window_size: int = 5) -> np.ndarray:
    """
    Apply smoothing to a sequence of landmarks
    
    Args:
        landmarks_sequence: List of landmark arrays
        window_size: Size of smoothing window
        
    Returns:
        Smoothed landmarks
    """
    if not landmarks_sequence:
        return None
    
    # Take the last window_size landmarks
    recent_landmarks = landmarks_sequence[-window_size:]
    
    # Calculate moving average
    smoothed = np.mean(recent_landmarks, axis=0)
    
    return smoothed

def validate_landmarks(landmarks: np.ndarray) -> bool:
    """
    Validate if landmarks are reasonable
    
    Args:
        landmarks: Hand landmarks array
        
    Returns:
        True if landmarks are valid, False otherwise
    """
    if landmarks is None:
        return False
    
    # Check if landmarks have the correct shape
    if len(landmarks) != 63:  # 21 landmarks * 3 coordinates
        return False
    
    # Check for NaN or infinite values
    if np.any(np.isnan(landmarks)) or np.any(np.isinf(landmarks)):
        return False
    
    # Check if landmarks are within reasonable bounds
    landmarks_reshaped = landmarks.reshape(21, 3)
    x_coords = landmarks_reshaped[:, 0]
    y_coords = landmarks_reshaped[:, 1]
    
    # Check if coordinates are within reasonable range
    if np.any(x_coords < -1000) or np.any(x_coords > 1000):
        return False
    if np.any(y_coords < -1000) or np.any(y_coords > 1000):
        return False
    
    return True

def draw_fps(frame: np.ndarray, fps: float) -> np.ndarray:
    """
    Draw FPS on the frame
    
    Args:
        frame: Input frame
        fps: Current FPS
        
    Returns:
        Frame with FPS drawn
    """
    fps_text = f"FPS: {fps:.1f}"
    cv2.putText(
        frame, fps_text,
        (frame.shape[1] - 100, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
        (0, 255, 0), 2
    )
    return frame

def save_landmarks_to_file(landmarks: np.ndarray, filename: str, label: str = None):
    """
    Save landmarks to a file for training data collection
    
    Args:
        landmarks: Hand landmarks array
        filename: Output filename
        label: Optional label for the landmarks
    """
    data = {
        'landmarks': landmarks.tolist(),
        'label': label,
        'timestamp': np.datetime64('now').astype(str)
    }
    
    import json
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def load_landmarks_from_file(filename: str) -> Tuple[np.ndarray, str]:
    """
    Load landmarks from a file
    
    Args:
        filename: Input filename
        
    Returns:
        Tuple of (landmarks, label)
    """
    import json
    with open(filename, 'r') as f:
        data = json.load(f)
    
    landmarks = np.array(data['landmarks'])
    label = data.get('label', '')
    
    return landmarks, label

def get_system_info():
    """Print system information for debugging"""
    import platform
    import cv2
    
    print("=== System Information ===")
    print(f"Platform: {platform.platform()}")
    print(f"Python: {platform.python_version()}")
    print(f"OpenCV: {cv2.__version__}")
    
    try:
        import tensorflow as tf
        print(f"TensorFlow: {tf.__version__}")
    except ImportError:
        print("TensorFlow: Not installed")
    
    try:
        import mediapipe as mp
        print(f"MediaPipe: {mp.__version__}")
    except ImportError:
        print("MediaPipe: Not installed")

if __name__ == "__main__":
    # Create directories and show system info
    create_directories()
    get_system_info()
