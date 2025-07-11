# AI Sign Language Translator

An AI-powered sign language translator that uses computer vision and machine learning to recognize and translate sign language gestures into text in real-time.

## Features

- Real-time hand gesture detection using MediaPipe
- Machine learning model for sign language recognition
- Support for American Sign Language (ASL)
- Live video processing with OpenCV
- Text output of recognized signs
- Extensible architecture for adding new sign languages

## Technology Stack

- **Python 3.8+** - Core programming language
- **MediaPipe** - Hand landmark detection and tracking
- **TensorFlow/Keras** - Machine learning model training and inference
- **OpenCV** - Computer vision and video processing
- **NumPy** - Numerical computations
- **Matplotlib** - Data visualization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Yashasgitsit/AI-sign-language-translator.git
cd AI-sign-language-translator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the main application:
```bash
python main.py
```

This will start the webcam and begin detecting sign language gestures in real-time.

### Training a Custom Model

To train your own model with custom data:
```bash
python model.py --train --data-path data/training_data
```

## Project Structure

```
AI-sign-language-translator/
├── main.py                 # Main application entry point
├── sign_detector.py        # Hand detection and preprocessing
├── model.py               # ML model definition and training
├── translator.py          # Sign language translation logic
├── utils.py               # Utility functions
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── data/                  # Training and test data
├── models/                # Saved ML models
├── tests/                 # Unit tests
└── docs/                  # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MediaPipe team for the excellent hand tracking library
- TensorFlow team for the machine learning framework
- OpenCV community for computer vision tools


