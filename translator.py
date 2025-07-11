"""
Sign language translation module
"""

import cv2
import numpy as np
import tensorflow as tf
from collections import deque
from typing import Optional, Tuple
import config
import os

class SignTranslator:
    """Sign language translator using trained ML model"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize the translator
        
        Args:
            model_path: Path to the trained model file
        """
        self.model_path = model_path or config.MODEL_PATH
        self.model = None
        self.prediction_history = deque(maxlen=config.SMOOTHING_WINDOW)
        self.current_prediction = ""
        self.current_confidence = 0.0
        
        # Load model if it exists
        self._load_model()
        
    def _load_model(self):
        """Load the trained model"""
        if os.path.exists(self.model_path):
            try:
                self.model = tf.keras.models.load_model(self.model_path)
                print(f"Model loaded from {self.model_path}")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model = None
        else:
            print(f"Model file not found at {self.model_path}")
            print("Please train a model first using model.py")
            self.model = None
    
    def predict(self, landmarks: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Predict sign language gesture from landmarks
        
        Args:
            landmarks: Preprocessed hand landmarks
            
        Returns:
            Tuple of (predicted sign, confidence)
        """
        if self.model is None or landmarks is None:
            return None, 0.0
        
        try:
            # Reshape landmarks for model input
            landmarks_input = landmarks.reshape(1, -1)
            
            # Make prediction
            predictions = self.model.predict(landmarks_input, verbose=0)
            
            # Get the class with highest probability
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            # Convert to sign letter
            if confidence > config.GESTURE_THRESHOLD:
                predicted_sign = config.ASL_CLASSES[predicted_class_idx]
                
                # Add to prediction history for smoothing
                self.prediction_history.append((predicted_sign, confidence))
                
                # Apply smoothing
                smoothed_prediction, smoothed_confidence = self._smooth_predictions()
                
                self.current_prediction = smoothed_prediction
                self.current_confidence = smoothed_confidence
                
                return smoothed_prediction, smoothed_confidence
            
        except Exception as e:
            print(f"Prediction error: {e}")
        
        return None, 0.0
    
    def _smooth_predictions(self) -> Tuple[str, float]:
        """
        Smooth predictions using recent history
        
        Returns:
            Tuple of (smoothed prediction, average confidence)
        """
        if not self.prediction_history:
            return "", 0.0
        
        # Count occurrences of each prediction
        prediction_counts = {}
        total_confidence = 0.0
        
        for pred, conf in self.prediction_history:
            if pred in prediction_counts:
                prediction_counts[pred] += 1
            else:
                prediction_counts[pred] = 1
            total_confidence += conf
        
        # Get most frequent prediction
        most_frequent = max(prediction_counts, key=prediction_counts.get)
        avg_confidence = total_confidence / len(self.prediction_history)
        
        return most_frequent, avg_confidence
    
    def draw_results(self, frame: np.ndarray, prediction: str, confidence: float) -> np.ndarray:
        """
        Draw prediction results on the frame
        
        Args:
            frame: Input frame
            prediction: Predicted sign
            confidence: Prediction confidence
            
        Returns:
            Frame with drawn results
        """
        output_frame = frame.copy()
        
        # Draw prediction text
        if prediction:
            text = f"Sign: {prediction} ({confidence:.2f})"
            cv2.putText(
                output_frame, text, (10, 30),
                config.TEXT_FONT, config.TEXT_SCALE,
                config.TEXT_COLOR, config.TEXT_THICKNESS
            )
        else:
            text = "No sign detected"
            cv2.putText(
                output_frame, text, (10, 30),
                config.TEXT_FONT, config.TEXT_SCALE,
                (0, 0, 255), config.TEXT_THICKNESS  # Red color
            )
        
        # Draw instructions
        instructions = [
            "Press 'q' to quit",
            "Press 'r' to reset",
            "Press 's' to save prediction"
        ]
        
        for i, instruction in enumerate(instructions):
            y_pos = output_frame.shape[0] - 60 + (i * 20)
            cv2.putText(
                output_frame, instruction, (10, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 1
            )
        
        # Draw model status
        model_status = "Model: Loaded" if self.model else "Model: Not loaded"
        cv2.putText(
            output_frame, model_status, (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
            (0, 255, 0) if self.model else (0, 0, 255), 1
        )
        
        return output_frame
    
    def reset(self):
        """Reset the translator state"""
        self.prediction_history.clear()
        self.current_prediction = ""
        self.current_confidence = 0.0
    
    def get_current_prediction(self) -> Tuple[str, float]:
        """
        Get the current prediction and confidence
        
        Returns:
            Tuple of (current prediction, confidence)
        """
        return self.current_prediction, self.current_confidence
