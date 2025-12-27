"""
Main Window - Clean & Fixed Layout
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QApplication, QFrame, QScrollArea)
from PyQt5.QtCore import Qt
from ui.components import (VideoWidget, StatusCard, GestureInfoCard, 
                           ModeSelector, ControlPanel,
                           VoiceControlPanel, VoiceStatusCard)


class MainWindow(QMainWindow):
    """Redesigned Main Window with Fixed Layout"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        self.setWindowTitle("AI Gesture Control System")
        self.setGeometry(50, 50, 1600, 900)
        
        # Dark theme
        self.setStyleSheet("""
            QMainWindow {
                background: #0f172a;
            }
            * {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        self._init_ui()
        self._center_window()
    
    def _init_ui(self):
        """Initialize UI with proper spacing"""
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(16, 16, 16, 16)
        
        # === HEADER ===
        header = self._create_header()
        main_layout.addWidget(header)
        
        # === CONTENT (3 columns) ===
        content = QHBoxLayout()
        content.setSpacing(16)
        
        # LEFT: Video (45%)
        left_col = self._create_left_column()
        content.addWidget(left_col, 45)
        
        # CENTER: Gesture & Voice (30%)
        center_col = self._create_center_column()
        content.addWidget(center_col, 30)
        
        # RIGHT: Controls (25%)
        right_col = self._create_right_column()
        content.addWidget(right_col, 25)
        
        main_layout.addLayout(content, 1)
    
    def _create_header(self):
        """Header bar"""
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background: #1e293b;
                border-bottom: 2px solid #4f46e5;
                border-radius: 12px;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)
        
        # Title
        title = QLabel("🎯 AI Gesture Control System")
        title.setStyleSheet("""
            color: #f1f5f9;
            font-size: 22px;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Status
        self.status_indicator = QLabel("⚫ OFFLINE")
        self.status_indicator.setStyleSheet("""
            background: #334155;
            color: #94a3b8;
            padding: 8px 20px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: bold;
        """)
        layout.addWidget(self.status_indicator)
        
        return header
    
    def _create_left_column(self):
        """Left column - Video + Stats"""
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Video
        self.video_widget = VideoWidget()
        layout.addWidget(self.video_widget, 2)
        
        # Stats row - proper blocks
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)
        
        self.fps_card = StatusCard("FPS", "⚡")
        self.hands_card = StatusCard("Hands", "🖐️")
        self.actions_card = StatusCard("Actions", "✅")
        
        stats_layout.addWidget(self.fps_card, 1)
        stats_layout.addWidget(self.hands_card, 1)
        stats_layout.addWidget(self.actions_card, 1)
        
        layout.addLayout(stats_layout, 1)
        
        return container
    
    def _create_center_column(self):
        """Center column - Gesture & Voice"""
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Gesture card
        self.gesture_card = GestureInfoCard()
        layout.addWidget(self.gesture_card)
        
        # Voice status
        self.voice_status = VoiceStatusCard()
        layout.addWidget(self.voice_status)
        
        layout.addStretch()
        
        return container
    
    def _create_right_column(self):
        """Right column - Controls"""
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #1e293b;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #4f46e5;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #6366f1;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("""
            QWidget {
                background: #0f172a;
            }
        """)
        layout = QVBoxLayout(scroll_widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Control panel
        self.control_panel = ControlPanel()
        layout.addWidget(self.control_panel)
        
        # Mode selector
        self.mode_selector = ModeSelector()
        layout.addWidget(self.mode_selector)
        
        # Voice control
        self.voice_control = VoiceControlPanel()
        layout.addWidget(self.voice_control)
        
        layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        return scroll
    
    def _center_window(self):
        screen = QApplication.desktop().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    # === UPDATE METHODS ===
    
    def update_video_frame(self, frame):
        self.video_widget.update_frame(frame)
    
    def update_fps(self, fps):
        self.fps_card.update_value(fps)
    
    def update_hands_detected(self, count):
        self.hands_card.update_value(count)
    
    def update_gesture(self, gesture_name, confidence):
        self.gesture_card.update_gesture(gesture_name, confidence)
    
    def update_actions_count(self, count):
        self.actions_card.update_value(count)
    
    def add_log_message(self, message):
        pass  # Log removed for cleaner UI
    
    def update_voice_status(self, listening, text=""):
        self.voice_status.update_status(listening)
        if text:
            self.voice_status.update_text(text)
    
    def set_status(self, is_online):
        if is_online:
            self.status_indicator.setText("🟢 ONLINE")
            self.status_indicator.setStyleSheet("""
                background: rgba(16, 185, 129, 0.2);
                color: #10b981;
                padding: 8px 20px;
                border-radius: 16px;
                font-size: 12px;
                font-weight: bold;
                border: 1px solid rgba(16, 185, 129, 0.5);
            """)
        else:
            self.status_indicator.setText("⚫ OFFLINE")
            self.status_indicator.setStyleSheet("""
                background: #334155;
                color: #94a3b8;
                padding: 8px 20px;
                border-radius: 16px;
                font-size: 12px;
                font-weight: bold;
            """)