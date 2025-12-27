"""
Main Application Entry Point
AI Gesture Control System with Voice Recognition
"""

import sys
import json
import cv2
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon

from modules.hand_detector import HandDetector
from modules.gesture_recognizer import GestureRecognizer
from modules.system_controller import SystemController, ControlMode
from modules.voice_controller import VoiceController
from ui.main_window import MainWindow
from utils.logger import logger


class GestureControlThread(QThread):
    """Background thread for gesture processing"""
    
    frame_ready = pyqtSignal(object)  # Processed frame
    gesture_detected = pyqtSignal(str, float)  # Gesture name, confidence
    hands_detected = pyqtSignal(int)  # Number of hands
    fps_updated = pyqtSignal(int)  # FPS value
    
    def __init__(self, config, hand_detector, gesture_recognizer):
        super().__init__()
        self.config = config
        self.hand_detector = hand_detector
        self.gesture_recognizer = gesture_recognizer
        self.is_running = False
        self.cap = None
    
    def run(self):
        """Main processing loop"""
        logger.info("Starting gesture control thread...")
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            logger.error("Failed to open camera")
            # Try alternative camera indices
            for i in range(1, 3):
                logger.info(f"Trying camera index {i}...")
                self.cap = cv2.VideoCapture(i)
                if self.cap.isOpened():
                    break
        
        if not self.cap.isOpened():
            logger.error("No camera available!")
            return
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['camera']['width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['camera']['height'])
        self.cap.set(cv2.CAP_PROP_FPS, self.config['camera']['fps'])
        
        self.is_running = True
        logger.info("Camera initialized successfully")
        
        while self.is_running:
            ret, frame = self.cap.read()
            
            if not ret:
                logger.warning("Failed to read frame from camera")
                continue
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process frame with hand detector
            processed_frame, hands_data = self.hand_detector.process_frame(frame)
            
            # Emit hands detected count
            self.hands_detected.emit(len(hands_data))
            
            # Recognize gesture if hands detected
            gesture_name = None
            confidence = 0.0
            
            if hands_data:
                gesture_name, confidence = self.gesture_recognizer.recognize_gesture(hands_data)
            
            # Emit gesture information
            if gesture_name:
                self.gesture_detected.emit(gesture_name, confidence)
            else:
                self.gesture_detected.emit("", 0.0)
            
            # Emit FPS
            fps = self.hand_detector.get_fps()
            self.fps_updated.emit(fps)
            
            # Emit processed frame
            self.frame_ready.emit(processed_frame)
        
        # Cleanup
        if self.cap:
            self.cap.release()
        logger.info("Gesture control thread stopped")
    
    def stop(self):
        """Stop the processing thread"""
        logger.info("Stopping gesture control thread...")
        self.is_running = False
        self.wait()


class GestureControlApp:
    """Main application controller"""
    
    def __init__(self):
        """Initialize application"""
        logger.info("Initializing Gesture Control System...")
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize modules
        logger.info("Initializing hand detector...")
        self.hand_detector = HandDetector(self.config)
        
        logger.info("Initializing gesture recognizer...")
        self.gesture_recognizer = GestureRecognizer(self.config)
        
        logger.info("Initializing system controller...")
        self.system_controller = SystemController(self.config)
        
        logger.info("Initializing voice controller...")
        self.voice_controller = VoiceController(self.config)
        
        # Create GUI
        self.app = QApplication(sys.argv)
        self.window = MainWindow(self.config)
        
        # Processing thread
        self.processing_thread = None
        self.voice_thread = None
        
        # Action counter
        self.actions_executed = 0
        
        # Voice recognition state
        self.voice_enabled = False
        
        # Connect signals
        self._connect_signals()
        
        logger.info("Application initialized successfully")
    
    def _load_config(self):
        """Load configuration from JSON file"""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            logger.info("Configuration loaded successfully")
            return config
        except FileNotFoundError:
            logger.error("config.json not found!")
            QMessageBox.critical(
                None,
                "Configuration Error",
                "config.json file not found!\nPlease ensure the file exists."
            )
            sys.exit(1)
    
    def _connect_signals(self):
        """Connect GUI signals to handlers"""
        # Control panel signals
        self.window.control_panel.start_clicked.connect(self.start_detection)
        self.window.control_panel.stop_clicked.connect(self.stop_detection)
        
        # Mode selector signal
        self.window.mode_selector.mode_changed.connect(self.change_mode)
        
        # Voice control signal
        self.window.voice_control.voice_toggle.connect(self.toggle_voice_control)
    
    def start_detection(self):
        """Start gesture detection"""
        logger.info("Starting gesture detection...")
        
        # Create and start processing thread
        self.processing_thread = GestureControlThread(
            self.config,
            self.hand_detector,
            self.gesture_recognizer
        )
        
        # Connect thread signals
        self.processing_thread.frame_ready.connect(self.on_frame_ready)
        self.processing_thread.gesture_detected.connect(self.on_gesture_detected)
        self.processing_thread.hands_detected.connect(self.on_hands_detected)
        self.processing_thread.fps_updated.connect(self.on_fps_updated)
        
        # Start thread
        self.processing_thread.start()
        
        # Update UI
        self.window.control_panel.set_running(True)
        self.window.set_status(True)
        self.window.add_log_message("✓ Detection started successfully")
        
        logger.info("Detection started")
    
    def stop_detection(self):
        """Stop gesture detection"""
        logger.info("Stopping gesture detection...")
        
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.stop()
            self.processing_thread = None
        
        # Update UI
        self.window.control_panel.set_running(False)
        self.window.set_status(False)
        self.window.add_log_message("⬛ Detection stopped")
        
        logger.info("Detection stopped")
    
    def change_mode(self, mode):
        """Change control mode"""
        logger.info(f"Changing mode to: {mode}")
        
        self.system_controller.set_mode(mode)
        self.window.add_log_message(f"🔄 Mode changed to: {mode.upper()}")
        
        logger.info(f"Mode changed to: {mode}")
    
    def on_frame_ready(self, frame):
        """Handle processed frame from thread"""
        self.window.update_video_frame(frame)
    
    def on_gesture_detected(self, gesture_name, confidence):
        """Handle detected gesture"""
        self.window.update_gesture(gesture_name, confidence)
        
        if gesture_name:
            # Execute corresponding action
            success = self.system_controller.execute_gesture(gesture_name)
            
            if success:
                self.actions_executed += 1
                self.window.update_actions_count(self.actions_executed)
                
                # Get recent action history
                history = self.system_controller.get_action_history(1)
                if history:
                    self.window.add_log_message(history[0])
    
    def on_hands_detected(self, count):
        """Handle hands detected count"""
        self.window.update_hands_detected(count)
    
    def on_fps_updated(self, fps):
        """Handle FPS update"""
        self.window.update_fps(fps)
    
    def toggle_voice_control(self, enabled):
        """Toggle voice recognition control"""
        if enabled:
            logger.info("Enabling voice control...")
            self.voice_enabled = True
            self.window.update_voice_status(False, "🎤 Ready to listen... Speak commands now!")
            self.window.add_log_message("✅ Voice control enabled")
            
            # Start voice listening in background
            def voice_listener():
                try:
                    while self.voice_enabled:
                        self.window.update_voice_status(True)
                        command = self.voice_controller.listen()
                        if command:
                            self.window.update_voice_status(False, f"📝 {command}")
                            self.window.add_log_message(f"🎤 Voice: {command}")
                            # Process command
                            self.voice_controller.process_command(command)
                        else:
                            self.window.update_voice_status(False, "No command detected")
                except Exception as e:
                    logger.error(f"Voice error: {e}")
                    self.window.update_voice_status(False, f"Error: {str(e)}")
            
            import threading
            voice_thread = threading.Thread(target=voice_listener, daemon=True)
            voice_thread.start()
            
        else:
            logger.info("Disabling voice control...")
            self.voice_enabled = False
            self.window.update_voice_status(False, "Voice control disabled")
            self.window.add_log_message("⬛ Voice control disabled")
    
    def run(self):
        """Run the application"""
        logger.info("Starting application GUI...")
        self.window.show()
        
        # Handle application exit
        self.app.aboutToQuit.connect(self.cleanup)
        
        sys.exit(self.app.exec_())
    
    def cleanup(self):
        """Cleanup resources before exit"""
        logger.info("Cleaning up resources...")
        
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.stop()
        
        if self.voice_controller:
            self.voice_controller.stop_listening()
        
        self.hand_detector.release()
        
        logger.info("Application closed successfully")


def main():
    """Main entry point"""
    try:
        app = GestureControlApp()
        app.run()
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        QMessageBox.critical(
            None,
            "Fatal Error",
            f"An unexpected error occurred:\n{str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()