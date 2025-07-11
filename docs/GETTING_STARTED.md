# Getting Started with AI Sign Language Translator

## Overview

This project implements an AI-powered sign language translator that can recognize American Sign Language (ASL) gestures in real-time using computer vision and machine learning techniques.

## Architecture

The system consists of several key components:

1. **Sign Detector** (`sign_detector.py`): Uses MediaPipe to detect and track hand landmarks
2. **Translator** (`translator.py`): Processes landmarks and predicts sign language gestures
3. **Model** (`model.py`): Neural network for gesture classification
4. **Main Application** (`main.py`): Coordinates all components and handles user interface

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Yashasgitsit/AI-sign-language-translator.git
cd AI-sign-language-translator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Application

```bash
# Run with default settings
python main.py

# Run with specific camera
python main.py --camera 1

# Run without display (for testing)
python main.py --no-display
```

### 3. Training a Model

Currently, the project includes a placeholder for model training. To implement actual training:

1. Collect training data by recording hand gestures for each ASL letter
2. Preprocess the data using the `sign_detector.py` module
3. Train the model using `model.py`

```bash
# Train model (placeholder implementation)
python model.py --train --data-path data/training_data
```

## Key Features

### Real-time Detection
- Uses MediaPipe for fast and accurate hand landmark detection
- Processes video frames at 30 FPS
- Provides immediate visual feedback

### Machine Learning
- Neural network architecture optimized for gesture recognition
- Supports 26 ASL alphabet signs (A-Z)
- Includes prediction smoothing for stability

### User Interface
- Live video display with overlay information
- Keyboard controls for interaction
- Visual indicators for model status and predictions

## Configuration

The `config.py` file contains all configurable parameters:

- Camera settings (resolution, FPS)
- MediaPipe parameters (confidence thresholds)
- Model settings (input size, number of classes)
- Display settings (colors, fonts)

## Data Collection

To train your own model, you'll need to collect training data:

1. Run the application in data collection mode
2. Record multiple samples of each ASL letter
3. Ensure good lighting and clear hand visibility
4. Vary hand positions and orientations for robustness

## Troubleshooting

### Common Issues

1. **Camera not detected**: Check camera index in config or use `--camera` parameter
2. **Model not found**: Train a model first using `model.py --train`
3. **Poor detection**: Ensure good lighting and clear background
4. **Low FPS**: Reduce camera resolution or close other applications

### Performance Tips

- Use good lighting conditions
- Keep hands clearly visible against contrasting background
- Avoid rapid movements for better tracking
- Ensure camera is stable and at appropriate distance

## Next Steps

1. Implement actual data collection and training pipeline
2. Add support for dynamic gestures (words/phrases)
3. Improve model architecture for better accuracy
4. Add web interface for easier access
5. Support for multiple sign languages

## Contributing

See the main README.md for contribution guidelines.
