"""
UI Components - Clean Modern Design
"""

from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QSizePolicy, QWidget, QProgressBar)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
import cv2


class VideoWidget(QLabel):
    """Video display widget"""
    def __init__(self):
        super().__init__()
        self.setMinimumSize(640, 480)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        
        self.setStyleSheet("""
            QLabel {
                background: #1a1f36;
                border: 2px solid #4f46e5;
                border-radius: 12px;
                color: #94a3b8;
                font-size: 16px;
                font-weight: 600;
            }
        """)
        
        self.setText("📹 Camera Feed\n\nClick 'Start Detection' to begin")
    
    def update_frame(self, frame):
        if frame is not None:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            from PyQt5.QtGui import QImage
            img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            scaled = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled)


class StatusCard(QFrame):
    """Large status card with proper styling"""
    def __init__(self, title, icon="📊"):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                border: 2px solid #4f46e5;
                border-radius: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 20, 24, 20)
        
        # Title
        title_label = QLabel(f"{icon} {title}")
        title_label.setStyleSheet("""
            color: #94a3b8;
            font-size: 14px;
            font-weight: 700;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Value - much larger
        self.value = QLabel("--")
        self.value.setStyleSheet("""
            color: #4f46e5;
            font-size: 56px;
            font-weight: 900;
        """)
        self.value.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value)
    
    def update_value(self, val):
        self.value.setText(str(val))


class GestureInfoCard(QFrame):
    """Gesture display card - clean and focused"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: #1e293b;
                border: 2px solid #4f46e5;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 24, 20, 24)
        
        # Title
        title = QLabel("🎯 Current Gesture")
        title.setStyleSheet("""
            color: #f1f5f9;
            font-size: 14px;
            font-weight: 700;
        """)
        layout.addWidget(title)
        
        # Gesture name - large and clear
        self.gesture = QLabel("None Detected")
        self.gesture.setAlignment(Qt.AlignCenter)
        self.gesture.setWordWrap(True)
        self.gesture.setStyleSheet("""
            color: #4f46e5;
            font-size: 48px;
            font-weight: 900;
            padding: 20px 0;
        """)
        layout.addWidget(self.gesture)
    
    def update_gesture(self, name, conf):
        if name and name != "":
            gesture_text = name.replace('_', ' ').title()
            self.gesture.setText(gesture_text)
        else:
            self.gesture.setText("None Detected")


class ControlPanel(QFrame):
    """Control buttons panel"""
    start_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setFixedHeight(160)
        self.setStyleSheet("""
            QFrame {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 16, 20, 16)
        
        # Title
        title = QLabel("⚙️ System Controls")
        title.setStyleSheet("""
            color: #f1f5f9;
            font-size: 14px;
            font-weight: 700;
        """)
        layout.addWidget(title)
        
        # START BUTTON
        self.start_btn = QPushButton("▶ START DETECTION")
        self.start_btn.setFixedHeight(48)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: #059669;
            }
            QPushButton:disabled {
                background: #334155;
                color: #64748b;
            }
        """)
        self.start_btn.clicked.connect(self.start_clicked.emit)
        layout.addWidget(self.start_btn)
        
        # STOP BUTTON
        self.stop_btn = QPushButton("⏹ STOP DETECTION")
        self.stop_btn.setFixedHeight(48)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: #ef4444;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: #dc2626;
            }
            QPushButton:disabled {
                background: #334155;
                color: #64748b;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_clicked.emit)
        layout.addWidget(self.stop_btn)
    
    def set_running(self, running):
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)


class ModeSelector(QFrame):
    """Mode selection panel"""
    mode_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setFixedHeight(210)
        self.setStyleSheet("""
            QFrame {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 16, 20, 16)
        
        # Title
        title = QLabel("🎮 Control Mode")
        title.setStyleSheet("""
            color: #f1f5f9;
            font-size: 14px;
            font-weight: 700;
        """)
        layout.addWidget(title)
        
        # Mode buttons
        self.buttons = {}
        modes = [
            ('slide', '📊 Slide Mode'),
            ('music', '🎵 Music Mode'),
            ('desktop', '🖥️ Desktop Mode'),
        ]
        
        self.current = 'slide'
        
        for mode_id, name in modes:
            btn = QPushButton(name)
            btn.setFixedHeight(42)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda x, m=mode_id: self._change_mode(m))
            layout.addWidget(btn)
            self.buttons[mode_id] = btn
        
        self._update_styles()
    
    def _change_mode(self, mode):
        self.current = mode
        self._update_styles()
        self.mode_changed.emit(mode)
    
    def _update_styles(self):
        for mode_id, btn in self.buttons.items():
            if mode_id == self.current:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #4f46e5, stop:1 #7c3aed);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: 700;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #0f172a;
                        color: #94a3b8;
                        border: 1px solid #334155;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: 600;
                    }
                    QPushButton:hover {
                        background: #1e293b;
                        border-color: #4f46e5;
                        color: #cbd5e1;
                    }
                """)


class VoiceStatusCard(QFrame):
    """Voice recognition status"""
    def __init__(self):
        super().__init__()
        self.setFixedHeight(140)
        self.setStyleSheet("""
            QFrame {
                background: #1e293b;
                border: 2px solid #06b6d4;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 16, 20, 16)
        
        # Title
        title = QLabel("🎤 Voice Recognition")
        title.setStyleSheet("""
            color: #f1f5f9;
            font-size: 14px;
            font-weight: 700;
        """)
        layout.addWidget(title)
        
        # Status
        self.status = QLabel("⚫ Standby")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("""
            color: #06b6d4;
            font-size: 16px;
            font-weight: 700;
        """)
        layout.addWidget(self.status)
        
        # Command text
        self.text = QLabel("No command detected")
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setWordWrap(True)
        self.text.setStyleSheet("""
            color: #cbd5e1;
            font-size: 12px;
            font-weight: 500;
        """)
        layout.addWidget(self.text)
    
    def update_status(self, listening):
        if listening:
            self.status.setText("🔴 Listening...")
            self.status.setStyleSheet("""
                color: #ef4444;
                font-size: 16px;
                font-weight: 700;
            """)
        else:
            self.status.setText("⚫ Standby")
            self.status.setStyleSheet("""
                color: #06b6d4;
                font-size: 16px;
                font-weight: 700;
            """)
    
    def update_text(self, text):
        self.text.setText(text if text else "No command detected")


class VoiceControlPanel(QFrame):
    """Voice control toggle"""
    voice_toggle = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.setFixedHeight(110)
        self.setStyleSheet("""
            QFrame {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 16, 20, 16)
        
        # Title
        title = QLabel("🎤 Voice Control")
        title.setStyleSheet("""
            color: #f1f5f9;
            font-size: 14px;
            font-weight: 700;
        """)
        layout.addWidget(title)
        
        # Toggle button
        self.toggle_btn = QPushButton("Enable Voice Control")
        self.toggle_btn.setFixedHeight(44)
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.clicked.connect(self._on_toggle)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background: #334155;
                color: #cbd5e1;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: #475569;
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #06b6d4, stop:1 #0891b2);
                color: white;
            }
        """)
        layout.addWidget(self.toggle_btn)
    
    def _on_toggle(self):
        enabled = self.toggle_btn.isChecked()
        self.toggle_btn.setText("Disable Voice Control" if enabled else "Enable Voice Control")
        self.voice_toggle.emit(enabled)