"""
Main application for AI Sign Language Translator
"""

import cv2
import argparse
import sys
from sign_detector import SignDetector
from translator import SignTranslator
from utils import setup_logging
import config

def main():
    """Main function to run the sign language translator"""
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting AI Sign Language Translator")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AI Sign Language Translator')
    parser.add_argument('--camera', type=int, default=config.CAMERA_INDEX,
                       help='Camera index (default: 0)')
    parser.add_argument('--model', type=str, default=config.MODEL_PATH,
                       help='Path to trained model')
    parser.add_argument('--no-display', action='store_true',
                       help='Run without display (for testing)')
    
    args = parser.parse_args()
    
    try:
        # Initialize components
        detector = SignDetector()
        translator = SignTranslator(model_path=args.model)
        
        # Initialize camera
        cap = cv2.VideoCapture(args.camera)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, config.FPS)
        
        if not cap.isOpened():
            logger.error(f"Cannot open camera {args.camera}")
            return
        
        logger.info("Camera initialized successfully")
        logger.info("Press 'q' to quit, 'r' to reset, 's' to save current prediction")
        
        # Main processing loop
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.error("Failed to read frame from camera")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect hand landmarks
            landmarks, processed_frame = detector.detect_landmarks(frame)
            
            # Translate if landmarks are detected
            prediction = None
            confidence = 0.0
            
            if landmarks is not None:
                prediction, confidence = translator.predict(landmarks)
            
            # Draw results on frame
            display_frame = translator.draw_results(
                processed_frame, prediction, confidence
            )
            
            # Display frame (if not in no-display mode)
            if not args.no_display:
                cv2.imshow(config.WINDOW_NAME, display_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    translator.reset()
                    logger.info("Translator reset")
                elif key == ord('s') and prediction:
                    logger.info(f"Current prediction: {prediction} (confidence: {confidence:.2f})")
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Cleanup
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()
        logger.info("Application closed")

if __name__ == "__main__":
    main()
