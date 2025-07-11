"""
Machine learning model for sign language recognition
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import os
import argparse
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import config
from utils import setup_logging

class SignLanguageModel:
    """Neural network model for sign language classification"""
    
    def __init__(self):
        """Initialize the model"""
        self.model = None
        self.label_encoder = LabelEncoder()
        self.logger = setup_logging()
        
    def create_model(self, input_shape: tuple, num_classes: int) -> keras.Model:
        """
        Create a neural network model for sign language classification
        
        Args:
            input_shape: Shape of input features
            num_classes: Number of sign language classes
            
        Returns:
            Compiled Keras model
        """
        model = keras.Sequential([
            # Input layer
            layers.Input(shape=input_shape),
            
            # Dense layers with dropout for regularization
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            
            # Output layer
            layers.Dense(num_classes, activation='softmax')
        ])
        
        # Compile the model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=config.LEARNING_RATE),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.logger.info(f"Model created with input shape: {input_shape}")
        self.logger.info(f"Number of classes: {num_classes}")
        
        return model
    
    def prepare_data(self, data_path: str):
        """
        Prepare training data from the specified path
        
        Args:
            data_path: Path to training data directory
            
        Returns:
            Tuple of (X_train, X_val, y_train, y_val)
        """
        # This is a placeholder for data preparation
        # In a real implementation, you would load your dataset here
        
        self.logger.info(f"Preparing data from: {data_path}")
        
        # For demonstration, create dummy data
        # Replace this with actual data loading logic
        num_samples = 1000
        input_features = 63  # 21 landmarks * 3 coordinates
        
        X = np.random.randn(num_samples, input_features)
        y = np.random.randint(0, config.NUM_CLASSES, num_samples)
        
        # Convert labels to categorical
        y_categorical = keras.utils.to_categorical(y, config.NUM_CLASSES)
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y_categorical, 
            test_size=config.VALIDATION_SPLIT,
            random_state=42,
            stratify=y
        )
        
        self.logger.info(f"Training samples: {len(X_train)}")
        self.logger.info(f"Validation samples: {len(X_val)}")
        
        return X_train, X_val, y_train, y_val
    
    def train(self, data_path: str, save_path: str = None):
        """
        Train the sign language model
        
        Args:
            data_path: Path to training data
            save_path: Path to save the trained model
        """
        save_path = save_path or config.MODEL_PATH
        
        # Prepare data
        X_train, X_val, y_train, y_val = self.prepare_data(data_path)
        
        # Create model
        input_shape = (X_train.shape[1],)
        self.model = self.create_model(input_shape, config.NUM_CLASSES)
        
        # Print model summary
        self.model.summary()
        
        # Define callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            ),
            keras.callbacks.ModelCheckpoint(
                save_path,
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train the model
        self.logger.info("Starting training...")
        
        history = self.model.fit(
            X_train, y_train,
            batch_size=config.BATCH_SIZE,
            epochs=config.EPOCHS,
            validation_data=(X_val, y_val),
            callbacks=callbacks,
            verbose=1
        )
        
        # Save final model
        self.model.save(save_path)
        self.logger.info(f"Model saved to: {save_path}")
        
        return history
    
    def evaluate(self, test_data_path: str, model_path: str = None):
        """
        Evaluate the trained model
        
        Args:
            test_data_path: Path to test data
            model_path: Path to saved model
        """
        model_path = model_path or config.MODEL_PATH
        
        if not os.path.exists(model_path):
            self.logger.error(f"Model not found at: {model_path}")
            return
        
        # Load model
        self.model = keras.models.load_model(model_path)
        self.logger.info(f"Model loaded from: {model_path}")
        
        # Prepare test data (placeholder)
        # Replace with actual test data loading
        X_test = np.random.randn(100, 63)
        y_test = keras.utils.to_categorical(
            np.random.randint(0, config.NUM_CLASSES, 100),
            config.NUM_CLASSES
        )
        
        # Evaluate
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        
        self.logger.info(f"Test Loss: {test_loss:.4f}")
        self.logger.info(f"Test Accuracy: {test_accuracy:.4f}")

def main():
    """Main function for training and evaluation"""
    parser = argparse.ArgumentParser(description='Sign Language Model Training')
    parser.add_argument('--train', action='store_true', help='Train the model')
    parser.add_argument('--evaluate', action='store_true', help='Evaluate the model')
    parser.add_argument('--data-path', type=str, default=config.TRAINING_DATA_DIR,
                       help='Path to training data')
    parser.add_argument('--model-path', type=str, default=config.MODEL_PATH,
                       help='Path to save/load model')
    
    args = parser.parse_args()
    
    model = SignLanguageModel()
    
    if args.train:
        model.train(args.data_path, args.model_path)
    elif args.evaluate:
        model.evaluate(args.data_path, args.model_path)
    else:
        print("Please specify --train or --evaluate")

if __name__ == "__main__":
    main()
