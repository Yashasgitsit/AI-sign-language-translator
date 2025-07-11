# Yashas's Development Projects

This repository contains multiple projects showcasing different technologies and applications.

## 🤖 AI Sign Language Translator

An AI-powered sign language translator that uses computer vision and machine learning to recognize and translate sign language gestures into text in real-time.

## 🔗 AWS Serverless URL Shortener

A serverless URL shortener built with AWS Lambda, API Gateway, and DynamoDB for creating and managing short URLs.

---

## AI Sign Language Translator

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

---

## 🔗 AWS Serverless URL Shortener

### Overview

A serverless URL shortener service built with AWS Lambda, API Gateway, and DynamoDB. This application provides:

- **URL Shortening**: Convert long URLs into short, shareable links
- **Redirection**: Automatic redirection from short URLs to original URLs
- **Analytics**: Click tracking and usage statistics
- **Serverless Architecture**: Pay-per-use, auto-scaling infrastructure

### Features

- ✅ Real-time URL shortening
- ✅ Custom short codes (3-8 characters)
- ✅ Click tracking and analytics
- ✅ CORS-enabled API
- ✅ Responsive web interface
- ✅ AWS serverless infrastructure
- ✅ Cost-effective pay-per-use model

### Quick Start

1. **Navigate to URL Shortener directory:**
```bash
cd url-shortener
```

2. **Deploy using AWS SAM:**
```bash
./deploy.sh
```

3. **Access the web interface:**
Visit the S3 frontend URL provided after deployment

### API Usage

**Create Short URL:**
```bash
curl -X POST https://your-api-gateway-url/ \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com/very-long-url"}'
```

**Use Short URL:**
```
https://your-api-gateway-url/abc123
```

### Architecture

```
Frontend (S3) → API Gateway → Lambda Functions → DynamoDB
```

### Documentation

- [Complete Setup Guide](url-shortener/README.md)
- [API Documentation](url-shortener/docs/API.md)
- [Deployment Instructions](url-shortener/deploy.sh)

---

## 📁 Repository Structure

```
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
│
├── AI Sign Language Translator/
│   ├── main.py                  # Main application
│   ├── sign_detector.py         # Hand detection
│   ├── translator.py            # Translation engine
│   ├── model.py                 # ML model training
│   ├── config.py                # Configuration
│   ├── utils.py                 # Utilities
│   ├── requirements.txt         # Dependencies
│   ├── tests/                   # Unit tests
│   └── docs/                    # Documentation
│
└── url-shortener/
    ├── lambda/                  # AWS Lambda functions
    ├── frontend/                # Web interface
    ├── template.yaml            # AWS SAM template
    ├── deploy.sh                # Deployment script
    ├── tests/                   # Unit tests
    └── docs/                    # API documentation
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** for AI Sign Language Translator
- **AWS CLI** and **SAM CLI** for URL Shortener
- **Git** for version control

### Clone Repository

```bash
git clone https://github.com/Yashasgitsit/AI-sign-language-translator.git
cd AI-sign-language-translator
```

### Choose Your Project

**For AI Sign Language Translator:**
```bash
pip install -r requirements.txt
python main.py
```

**For URL Shortener:**
```bash
cd url-shortener
./deploy.sh
```

## 🛠️ Technologies Used

### AI Sign Language Translator
- Python, OpenCV, MediaPipe
- TensorFlow/Keras for ML
- NumPy, Matplotlib
- Real-time computer vision

### URL Shortener
- AWS Lambda (Python)
- API Gateway
- DynamoDB
- S3 for frontend hosting
- CloudWatch for monitoring

## 📊 Project Status

| Project | Status | Last Updated |
|---------|--------|--------------|
| AI Sign Language Translator | ✅ Active Development | 2024-01-01 |
| URL Shortener | ✅ Production Ready | 2024-01-01 |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

- **GitHub**: [@Yashasgitsit](https://github.com/Yashasgitsit)
- **Email**: yashas2004s@gmail.com

## 🌟 Acknowledgments

- AWS for serverless infrastructure
- MediaPipe and TensorFlow teams
- Open source community
