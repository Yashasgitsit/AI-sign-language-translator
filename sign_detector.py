"""
Sign detection module using MediaPipe for hand landmark detection
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple
import config

class SignDetector:
    """Hand landmark detection and preprocessing for sign language recognition"""
    
    def __init__(self):
        """Initialize MediaPipe hands solution"""
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize hands detector
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=config.MAX_NUM_HANDS,
            min_detection_confidence=config.MEDIAPIPE_CONFIDENCE,
            min_tracking_confidence=config.MEDIAPIPE_TRACKING_CONFIDENCE
        )
        
    def detect_landmarks(self, frame: np.ndarray) -> Tuple[Optional[np.ndarray], np.ndarray]:
        """
        Detect hand landmarks in the given frame
        
        Args:
            frame: Input image frame
            
        Returns:
            Tuple of (landmarks array, processed frame with drawings)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        # Create a copy of the frame for drawing
        output_frame = frame.copy()
        landmarks_array = None
        
        # Extract landmarks if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on the frame
                self.mp_drawing.draw_landmarks(
                    output_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Extract landmark coordinates
                landmarks_array = self._extract_landmarks(hand_landmarks, frame.shape)
                break  # Use only the first detected hand
        
        return landmarks_array, output_frame
    
    def _extract_landmarks(self, hand_landmarks, frame_shape: Tuple[int, int, int]) -> np.ndarray:
        """
        Extract and normalize hand landmarks
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            frame_shape: Shape of the input frame (height, width, channels)
            
        Returns:
            Normalized landmarks array
        """
        height, width = frame_shape[:2]
        landmarks = []
        
        for landmark in hand_landmarks.landmark:
            # Convert normalized coordinates to pixel coordinates
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            z = landmark.z
            landmarks.extend([x, y, z])
        
        return np.array(landmarks, dtype=np.float32)
    
    def preprocess_landmarks(self, landmarks: np.ndarray) -> np.ndarray:
        """
        Preprocess landmarks for model input
        
        Args:
            landmarks: Raw landmarks array
            
        Returns:
            Preprocessed landmarks ready for model input
        """
        if landmarks is None:
            return None
        
        # Reshape landmarks to (21, 3) for 21 hand landmarks with x, y, z coordinates
        landmarks_reshaped = landmarks.reshape(21, 3)
        
        # Normalize landmarks relative to wrist (landmark 0)
        wrist = landmarks_reshaped[0]
        normalized_landmarks = landmarks_reshaped - wrist
        
        # Calculate bounding box for further normalization
        x_coords = normalized_landmarks[:, 0]
        y_coords = normalized_landmarks[:, 1]
        
        x_min, x_max = np.min(x_coords), np.max(x_coords)
        y_min, y_max = np.min(y_coords), np.max(y_coords)
        
        # Avoid division by zero
        x_range = max(x_max - x_min, 1)
        y_range = max(y_max - y_min, 1)
        
        # Normalize to [-1, 1] range
        normalized_landmarks[:, 0] = (normalized_landmarks[:, 0] - x_min) / x_range * 2 - 1
        normalized_landmarks[:, 1] = (normalized_landmarks[:, 1] - y_min) / y_range * 2 - 1
        
        # Flatten for model input
        return normalized_landmarks.flatten()
    
    def get_hand_region(self, frame: np.ndarray, landmarks: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract hand region from frame based on landmarks
        
        Args:
            frame: Input frame
            landmarks: Hand landmarks
            
        Returns:
            Cropped hand region or None if extraction fails
        """
        if landmarks is None:
            return None
        
        # Reshape landmarks
        landmarks_reshaped = landmarks.reshape(21, 3)
        
        # Get bounding box coordinates
        x_coords = landmarks_reshaped[:, 0].astype(int)
        y_coords = landmarks_reshaped[:, 1].astype(int)
        
        x_min, x_max = np.min(x_coords), np.max(x_coords)
        y_min, y_max = np.min(y_coords), np.max(y_coords)
        
        # Add padding
        padding = 20
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(frame.shape[1], x_max + padding)
        y_max = min(frame.shape[0], y_max + padding)
        
        # Extract and resize hand region
        hand_region = frame[y_min:y_max, x_min:x_max]
        
        if hand_region.size > 0:
            hand_region = cv2.resize(hand_region, config.MODEL_INPUT_SIZE)
            return hand_region
        
        return None
