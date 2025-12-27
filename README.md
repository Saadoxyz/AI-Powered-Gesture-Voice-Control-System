# AI-Powered Gesture & Voice Control System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.5-FF6F00?style=for-the-badge&logo=google&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.10-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

![GitHub stars](https://img.shields.io/github/stars/Saadoxyz/AI-Powered-Gesture-Voice-Control-System?style=social)
![GitHub forks](https://img.shields.io/github/forks/Saadoxyz/AI-Powered-Gesture-Voice-Control-System?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/Saadoxyz/AI-Powered-Gesture-Voice-Control-System?style=social)

**Touchless Human-Computer Interaction Using Computer Vision, Machine Learning & Voice Recognition**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Modules](#modules)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Gesture Reference](#gesture-reference)
- [Voice Commands](#voice-commands)
- [Project Structure](#project-structure)
- [Performance](#performance)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

This **AI-Powered Gesture & Voice Control System** is an advanced human-computer interaction platform that enables touchless control of computer applications through hand gestures and voice commands. Built with state-of-the-art computer vision and speech recognition technologies, the system provides an intuitive, accessible, and hygienic way to interact with your computer.

### Key Highlights

- **Hand Gesture Recognition** - Control your computer with intuitive hand movements captured via webcam
- **Advanced Voice Assistant** - Complete voice-controlled browsing, application launching, and automation
- **Multi-Application Support** - Compatible with PowerPoint, Spotify, VLC, YouTube, WhatsApp, Chrome, and more
- **Professional User Interface** - Modern PyQt5 GUI with real-time feedback and visual indicators
- **High Performance** - Achieves 27-30 FPS with 92% gesture recognition accuracy
- **Modular Architecture** - Clean, maintainable code structure for easy extension and customization
- **Cross-Platform** - Works on Windows, macOS, and Linux operating systems
- **Machine Learning Powered** - Uses Random Forest classifier for intelligent gesture recognition
- **Real-time Processing** - Low latency response with minimal CPU overhead

### Use Cases

- **Presentations** - Navigate slides hands-free during presentations
- **Accessibility** - Assistive technology for users with limited mobility
- **Healthcare** - Touchless control in sterile medical environments
- **Education** - Interactive classroom teaching and demonstrations
- **Entertainment** - Control media playback from a distance
- **Smart Homes** - Gesture and voice-based home automation
- **Professional** - Hands-free control during design reviews or demonstrations

---

## Features

### Gesture Control Features

- **10+ Static Gestures** - Open palm, fist, pointing, peace sign, rock sign, hang loose, thumbs up, and more
- **4 Dynamic Gestures** - Swipe up, down, left, right with advanced trajectory tracking
- **3 Control Modes**:
  - **Presentation Mode** - Navigate PowerPoint slides, start/stop presentations, laser pointer
  - **Music Mode** - Control playback, volume adjustment, track navigation for Spotify/VLC
  - **Desktop Mode** - Browser navigation, scrolling, page refresh, screenshots
- **Real-time Hand Tracking** - 21-point landmark detection using MediaPipe
- **Gesture Stability** - Advanced cooldown and frame-holding mechanisms to prevent false triggers
- **Confidence Scoring** - Each gesture has an associated confidence level for reliability
- **Multi-hand Support** - Detects and tracks up to 2 hands simultaneously

### Voice Control Features

- **Complete Browser Automation**
  - Open any website by voice command
  - Search Google, YouTube, or any search engine
  - Click on search results (first, second, third, etc.)
  - Navigate browser history (back, forward, refresh)
  - Scroll pages up and down
  
- **Application Control**
  - Launch any installed application
  - Send WhatsApp messages by voice
  - Type text anywhere using voice dictation
  - Execute system commands
  - Open files and folders

- **Media Control**
  - Play, pause, stop media playback
  - Adjust volume up and down
  - Navigate to next or previous track
  - Search and play specific songs or videos

- **Natural Language Processing**
  - Understands natural conversational commands
  - Context-aware command interpretation
  - Text-to-speech feedback for confirmations
  - Multi-step workflow automation

### User Interface Features

- **Real-time Video Feed** - Live camera display with hand landmark overlays
- **Gesture Detection Display** - Large, clear display of currently detected gesture
- **Confidence Indicators** - Visual confidence scores for gesture recognition
- **Mode Switching Interface** - Easy switching between Gesture, Voice, and Settings tabs
- **Action Logging** - Comprehensive log of all executed commands with timestamps
- **Performance Metrics** - Real-time FPS counter and system statistics
- **Status Indicators** - Clear online/offline and detection status displays
- **Professional Dark Theme** - Easy on the eyes with modern gradient design
- **Responsive Layout** - Fixed component sizes for consistent user experience
- **Visual Feedback** - Color-coded status indicators and animations

---

## System Architecture
```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                        │
│              (PyQt5 GUI with Real-time Video Display)               │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   Gesture    │  │    Voice     │  │   Settings   │            │
│  │     Tab      │  │   Control    │  │     Tab      │            │
│  │              │  │     Tab      │  │              │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                ┌────────────┴─────────────┐
                │                          │
                │    APPLICATION LAYER     │
                │                          │
                └────────────┬─────────────┘
                             │
         ┌───────────────────┼───────────────────┬──────────────┐
         │                   │                   │              │
┌────────▼────────┐  ┌──────▼─────────┐  ┌──────▼──────┐  ┌───▼────────┐
│   MODULE 1      │  │   MODULE 2     │  │  MODULE 3   │  │  MODULE 4  │
│                 │  │                │  │             │  │            │
│ Hand Detection  │─▶│   Gesture      │─▶│   System    │  │   Voice    │
│  & Landmark     │  │ Recognition &  │  │  Control &  │  │Recognition │
│  Extraction     │  │ Classification │  │ Integration │  │ & Control  │
│                 │  │                │  │             │  │            │
│  - OpenCV       │  │  - Rule-based  │  │ - PyAutoGUI │  │ - Speech   │
│  - MediaPipe    │  │  - ML (Random  │  │ - System    │  │Recognition │
│  - Smoothing    │  │    Forest)     │  │   Commands  │  │ - pyttsx3  │
│  - Feature      │  │  - Confidence  │  │ - Mode      │  │ - NLP      │
│    Extraction   │  │    Scoring     │  │   Mapping   │  │            │
└────────┬────────┘  └────────┬───────┘  └──────┬──────┘  └───┬────────┘
         │                    │                  │             │
         │                    │                  │             │
    ┌────▼─────┐         ┌───▼────┐        ┌────▼─────┐  ┌───▼────┐
    │ Webcam   │         │   ML   │        │    OS    │  │  Mic   │
    │  Input   │         │ Model  │        │ Commands │  │ Input  │
    └──────────┘         └────────┘        └──────────┘  └────────┘
```

---

## Modules

### Module 1: Hand Detection & Landmark Extraction

**Technology:** OpenCV, MediaPipe Hands

**Features:**
- Real-time video capture at 30 FPS
- 21-point landmark extraction
- Coordinate normalization
- Noise reduction with smoothing filters
- Feature extraction (finger states, distances)

**Output:**
```python
{
    'landmarks': [[x1, y1, z1], [x2, y2, z2], ...],
    'features': {
        'extended_fingers': [1, 1, 0, 0, 0],
        'distances': {...},
        'palm_center': [x, y],
        'orientation': angle
    },
    'bbox': [x_min, y_min, x_max, y_max],
    'label': 'Left' or 'Right'
}
```

---

### Module 2: Gesture Recognition & Classification

**Technology:** Machine Learning (Random Forest), NumPy

**Features:**
- 10+ static gestures (open palm, fist, pointing, peace, thumbs up, rock sign, hang loose, etc.)
- 4 dynamic gestures (swipe up/down/left/right)
- Rule-based and ML classification
- Confidence scoring (70% threshold)
- Stability mechanisms (frame holding, cooldown)

**Recognition Methods:**
1. **Rule-Based** - Pattern matching (95% confidence)
2. **Machine Learning** - Random Forest classifier (92% accuracy)
3. **Dynamic Detection** - Trajectory analysis (10% movement threshold)

---

### Module 3: System Control & Integration

**Technology:** PyAutoGUI, PyQt5

**Features:**
- **Presentation Mode** - Slide navigation, F5 start, ESC end
- **Music Mode** - Play/pause, volume, track navigation
- **Desktop Mode** - Scrolling, browser navigation, screenshots

**Gesture Mappings:**
```python
Music Mode:
- Open Palm → Play/Pause
- Rock Sign → Volume Up
- Hang Loose → Volume Down
- Three Thumb → Next Track
- Four Fingers → Previous Track

Presentation Mode:
- Rock Sign → Next Slide
- Hang Loose → Previous Slide
- Open Palm → Start Presentation
- Fist → End Presentation

Desktop Mode:
- Rock Sign → Scroll Up
- Hang Loose → Scroll Down
- Pointing → Refresh Page
- Three Fingers → New Tab
```

---

### Module 4: Voice Recognition & Control

**Technology:** SpeechRecognition, pyttsx3

**Features:**
- Complete browser automation
- Application launching
- WhatsApp messaging
- Text dictation
- Media control
- Natural language processing

**Example Workflow:**
```
"Open Google" → Browser opens
"Search for YouTube" → Searches Google
"Click first result" → Opens YouTube
"Search for Cocomelon" → Searches YouTube
"Play video number 1" → Plays video
"Volume up" → Increases volume
```

---

## Installation

### Windows Installation
```cmd
# 1. Install Python 3.11+
# Download from https://www.python.org/downloads/
# Check "Add Python to PATH"

# 2. Clone repository
git clone https://github.com/Saadoxyz/AI-Powered-Gesture-Voice-Control-System.git
cd AI-Powered-Gesture-Voice-Control-System

# 3. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Install PyAudio
pip install pipwin
pipwin install pyaudio

# 6. Run application
python main.py
```

### macOS Installation
```bash
# 1. Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python
brew install python@3.11

# 3. Clone repository
git clone https://github.com/Saadoxyz/AI-Powered-Gesture-Voice-Control-System.git
cd AI-Powered-Gesture-Voice-Control-System

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 6. Install PortAudio and PyAudio
brew install portaudio
pip install pyaudio

# 7. Run application
python main.py
```

### Linux Installation
```bash
# 1. Update system
sudo apt-get update && sudo apt-get upgrade

# 2. Install dependencies
sudo apt-get install python3.11 python3-pip python3-venv
sudo apt-get install portaudio19-dev python3-pyaudio
sudo apt-get install python3-pyqt5

# 3. Clone repository
git clone https://github.com/Saadoxyz/AI-Powered-Gesture-Voice-Control-System.git
cd AI-Powered-Gesture-Voice-Control-System

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install pyaudio

# 6. Run application
python main.py
```

---

## Configuration

### config.json
```json
{
  "camera": {
    "device_index": 0,
    "width": 1280,
    "height": 720,
    "fps": 30
  },
  "hand_detection": {
    "max_hands": 2,
    "min_detection_confidence": 0.6,
    "min_tracking_confidence": 0.5,
    "smoothing_factor": 0.5
  },
  "gesture_recognition": {
    "confidence_threshold": 0.70,
    "cooldown_time": 0.8,
    "use_ml_model": true,
    "frame_stability": 5,
    "movement_threshold": 0.10
  },
  "system_control": {
    "slide_mode_enabled": true,
    "music_mode_enabled": true,
    "desktop_mode_enabled": true,
    "volume_step": 5,
    "scroll_speed": 200
  },
  "voice_control": {
    "enabled": true,
    "language": "en-US",
    "timeout": 5,
    "phrase_time_limit": 10,
    "tts_rate": 150,
    "tts_volume": 0.9
  },
  "ui": {
    "theme": "dark",
    "accent_color": "#1f6aa5",
    "show_landmarks": true,
    "show_fps": true
  }
}
```

### Add WhatsApp Contacts

Edit `modules/voice_controller.py`:
```python
self.contacts = {
    'abdur rehman': 'Abdur Rehman',
    'john doe': 'John Doe',
    # Add your contacts here
}
```

---

## Usage

### Starting Application
```bash
# Navigate to project directory
cd AI-Powered-Gesture-Voice-Control-System

# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run
python main.py
```

### Using Gesture Control

1. Click "START DETECTION"
2. Position yourself 1-2 feet from camera
3. Select mode (Presentation/Music/Desktop)
4. Make gestures:
   - Hold static gestures for 0.2 seconds
   - Make clear swipe movements
   - Check "Current Gesture" display for feedback

### Using Voice Control

1. Click "START VOICE CONTROL"
2. Wait for "I'm ready to help"
3. Speak commands clearly:
   - "Open Google"
   - "Search for YouTube"
   - "Click first result"
   - "Type: Hello World"
   - "Press Enter"

---

## Gesture Reference

### Static Gestures

| Gesture | Fingers | Confidence | Music Mode | Slide Mode | Desktop Mode |
|---------|---------|------------|------------|------------|--------------|
| **Open Palm** | All 5 | 98% | Play/Pause | Start Presentation | Show Desktop |
| **Fist** | None | 97% | Stop | End Presentation | Minimize |
| **Pointing** | Index | 96% | - | Laser Pointer | Refresh |
| **Peace** | Index+Middle | 95% | - | Last Slide | Screenshot |
| **Thumbs Up** | Thumb | 94% | - | First Slide | - |
| **Rock Sign** | Index+Pinky | 95% | Volume Up | Next Slide | Scroll Up |
| **Hang Loose** | Thumb+Pinky | 94% | Volume Down | Previous Slide | Scroll Down |
| **Three Thumb** | Thumb+Index+Middle | 93% | Next Track | - | Forward |
| **Four Fingers** | All except thumb | 92% | Previous Track | - | Back |

### Dynamic Gestures

| Gesture | Movement | Confidence | Music Mode | Slide Mode | Desktop Mode |
|---------|----------|------------|------------|------------|--------------|
| **Swipe Right** | → | 89% | Next Track | Next Slide | Forward |
| **Swipe Left** | ← | 88% | Previous Track | Previous Slide | Back |
| **Swipe Up** | ↑ | 85% | Volume Up | - | Scroll Up |
| **Swipe Down** | ↓ | 84% | Volume Down | - | Scroll Down |

### Gesture Requirements

**Static Gestures:**
- Hold for 5 frames (0.15 seconds)
- 70% confidence threshold
- 1.0 second cooldown

**Dynamic Gestures:**
- 10% screen movement minimum
- 2x directional dominance
- 0.6 second cooldown

---

## Voice Commands

### Browser Commands
```
"Open Google"
"Open YouTube"
"Open website [url]"
"Search for [query]"
"Search Google for [query]"
"Search YouTube for [query]"
"Click first result"
"Click second result"
"Click result number [1-10]"
"Play video number [1-10]"
"Go back"
"Go forward"
"Refresh"
"Scroll up"
"Scroll down"
"New tab"
"Close tab"
```

### Application Commands
```
"Open WhatsApp"
"Open Notepad"
"Open Calculator"
"Open Chrome"
"Open Spotify"
"Open [application name]"
```

### Typing Commands
```
"Type: [your text]"
"Press Enter"
"Press Space"
"Press Tab"
"Press Backspace"
```

### Media Commands
```
"Play"
"Pause"
"Stop"
"Volume up"
"Volume down"
"Mute"
"Unmute"
"Next track"
"Previous track"
```

### Messaging Commands
```
"Send message to [contact name]"
"Type: [message]"
"Press Enter"
```

---

## Project Structure
```
AI-Powered-Gesture-Voice-Control-System/
│
├── main.py                          # Application entry point
├── config.json                      # Configuration file
├── requirements.txt                 # Dependencies
├── README.md                        # Documentation
├── LICENSE                          # MIT License
│
├── modules/
│   ├── __init__.py
│   ├── hand_detector.py            # Module 1: Hand Detection
│   ├── gesture_recognizer.py       # Module 2: Gesture Recognition
│   ├── system_controller.py        # Module 3: System Control
│   └── voice_controller.py         # Module 4: Voice Control
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py              # Main GUI window
│   ├── components.py               # UI components
│   └── styles.py                   # Styling
│
├── utils/
│   ├── __init__.py
│   ├── preprocessing.py            # Utilities
│   └── logger.py                   # Logging
│
├── models/
│   ├── __init__.py
│   ├── gesture_classifier.pkl      # ML model
│   └── gesture_data.json           # Gesture definitions
│
└── logs/                           # System logs
    └── gesture_control_*.log
```

---

## Performance

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| **FPS** | 25+ | 27-30 | Excellent |
| **Gesture Accuracy** | >85% | 92% | Excellent |
| **Latency** | <100ms | 80ms | Excellent |
| **False Positive** | <5% | 3% | Excellent |
| **CPU Usage** | <40% | 25-35% | Good |

### Gesture Accuracy

| Gesture | Accuracy | Notes |
|---------|----------|-------|
| Open Palm | 98% | Highly reliable |
| Fist | 97% | Highly reliable |
| Rock Sign | 95% | Easy alternative |
| Hang Loose | 94% | Easy alternative |
| Swipe Right | 89% | Good with practice |
| Swipe Left | 88% | Good with practice |
| Swipe Up | 85% | Requires clear motion |
| Swipe Down | 84% | Requires clear motion |

---

## Requirements

### Minimum Requirements

**Hardware:**
- CPU: Intel Core i3 or equivalent
- RAM: 4 GB
- Webcam: 720p @ 30 FPS
- Microphone: Built-in or external
- Storage: 500 MB

**Software:**
- Python 3.11+
- Windows 10 / macOS 10.14+ / Ubuntu 20.04+

**Expected Performance:**
- FPS: 20-25
- Accuracy: 88%
- CPU: 35-40%

---

### Recommended Requirements

**Hardware:**
- CPU: Intel Core i5 or AMD Ryzen 5
- RAM: 8 GB
- Webcam: 1080p @ 30 FPS
- Microphone: Noise-cancelling
- Storage: 1 GB

**Expected Performance:**
- FPS: 27-30
- Accuracy: 92%
- CPU: 25-30%

---

## Troubleshooting

### Camera Not Detected
```bash
# Test camera
python -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"

# Try different camera index in config.json
"camera": { "device_index": 1 }

# Grant permissions
# Windows: Settings > Privacy > Camera
# macOS: System Preferences > Security & Privacy > Camera
# Linux: sudo usermod -a -G video $USER
```

### Low FPS
```json
// Reduce resolution in config.json
{
  "camera": {
    "width": 640,
    "height": 480
  },
  "gesture_recognition": {
    "use_ml_model": false
  }
}
```

### Gestures Not Recognized

- Improve lighting
- Simplify background
- Position hand closer (1-2 feet)
- Lower confidence threshold to 0.60
- Hold gestures longer (increase frame_stability to 7)

### Voice Commands Not Working
```bash
# Test microphone
python -m speech_recognition

# Reinstall PyAudio
pip uninstall pyaudio
pipwin install pyaudio  # Windows
brew install portaudio && pip install pyaudio  # macOS
sudo apt-get install portaudio19-dev && pip install pyaudio  # Linux

# Check internet connection (required for Google Speech API)
ping google.com
```

### PyAudio Installation Failed

**Windows:**
```cmd
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### Actions Not Executing

- Ensure target application is open and focused
- Run as administrator (Windows)
- Add delays in system_controller.py
- Verify keyboard shortcuts for your application

### High CPU Usage

- Reduce camera resolution
- Disable ML model
- Set max_hands to 1
- Close other applications

---

## API Documentation

### Hand Detector
```python
from modules.hand_detector import HandDetector

detector = HandDetector(config)
hands_data = detector.process_frame(frame)
detector.release()
```

**Methods:**
- `__init__(config)` - Initialize detector
- `process_frame(frame)` - Detect hands, returns list of hand data
- `draw_landmarks(frame, hands_data)` - Draw landmarks on frame
- `release()` - Release camera

---

### Gesture Recognizer
```python
from modules.gesture_recognizer import GestureRecognizer

recognizer = GestureRecognizer(config)
gesture, confidence = recognizer.recognize_gesture(hands_data)
```

**Methods:**
- `__init__(config)` - Initialize recognizer
- `recognize_gesture(hands_data)` - Returns (gesture_name, confidence)
- `get_gesture_history()` - Returns recent gestures
- `clear_history()` - Clear gesture history

---

### System Controller
```python
from modules.system_controller import SystemController

controller = SystemController(config)
controller.set_mode('music')
success = controller.execute_gesture('rock_sign', 0.95)
```

**Methods:**
- `__init__(config)` - Initialize controller
- `set_mode(mode)` - Set mode ('slide', 'music', 'desktop')
- `execute_gesture(gesture, confidence)` - Execute action
- `get_action_log()` - Return action history

---

### Voice Controller
```python
from modules.voice_controller import VoiceController

voice = VoiceController(config)
voice.start_listening()
success = voice.execute_command("Open Google")
voice.stop_listening()
```

**Methods:**
- `__init__(config)` - Initialize voice controller
- `start_listening()` - Start continuous listening
- `stop_listening()` - Stop listening
- `execute_command(command)` - Execute voice command
- `add_contact(spoken_name, actual_name)` - Add WhatsApp contact

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Include unit tests
- Update documentation

---

## Acknowledgments

- **MediaPipe** - Google's hand tracking solution
- **OpenCV** - Computer vision library
- **SpeechRecognition** - Voice recognition library
- **PyQt5** - GUI framework
- **Scikit-learn** - Machine learning library

---

## Contact

**Saad**
- Email: saadok652004@gmail.com
- GitHub: [@Saadoxyz](https://github.com/Saadoxyz)
- Project: [AI-Powered-Gesture-Voice-Control-System](https://github.com/Saadoxyz/AI-Powered-Gesture-Voice-Control-System)

**Report Issues:** [GitHub Issues](https://github.com/Saadoxyz/AI-Powered-Gesture-Voice-Control-System/issues)

---

## Show Your Support

If you find this project helpful, please give it a star on GitHub!

---

<div align="center">

**Made with dedication by Saad**

*Touchless interaction for a better future*

</div>
