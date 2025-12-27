"""
Module 3: System Control & Integration
Member 3: Automation Module
Handles system automation using PyAutoGUI
"""

import pyautogui
import time
import platform
import subprocess
from enum import Enum


class ControlMode(Enum):
    """Control modes for the system"""
    SLIDE_MODE = "slide"
    MUSIC_MODE = "music"
    DESKTOP_MODE = "desktop"
    CUSTOM_MODE = "custom"


class SystemController:
    def __init__(self, config):
        """Initialize System Controller"""
        self.config = config
        self.current_mode = ControlMode.SLIDE_MODE
        
        # PyAutoGUI settings
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.1  # Pause between actions
        
        # Action history
        self.action_history = []
        self.max_history = 50
        
        # Volume control settings
        self.volume_step = config['system_control']['volume_step']
        
        # Scroll settings
        self.scroll_speed = config['system_control']['scroll_speed']
        
        # Last action time (for logging)
        self.last_action_time = None
        
        # Gesture to action mapping
        self._initialize_gesture_mappings()
    
    def _initialize_gesture_mappings(self):
        """Initialize gesture to action mappings for each mode"""
        
        # Slide Mode Mappings
        self.slide_mappings = {
            'swipe_right': 'next_slide',
            'swipe_left': 'previous_slide',
            'open_palm': 'start_presentation',
            'fist': 'end_presentation',
            'pointing': 'laser_pointer',
            'thumbs_up': 'first_slide',
            'peace': 'last_slide',
            'rock_sign': 'next_slide',      # 🤘 Alternative for next
            'hang_loose': 'previous_slide',  # 🤙 Alternative for previous
        }
        
        # Music Mode Mappings
        self.music_mappings = {
            'open_palm': 'play_pause',
            'swipe_right': 'next_track',
            'swipe_left': 'previous_track',
            'swipe_up': 'volume_up',
            'swipe_down': 'volume_down',
            'fist': 'stop',
            'ok_sign': 'mute_unmute',
            'three_fingers': 'repeat_toggle',
            'rock_sign': 'volume_up',        # 🤘 EASY volume up!
            'hang_loose': 'volume_down',     # 🤙 EASY volume down!
            'three_thumb': 'next_track',     # 👌 Alternative next
            'four_fingers': 'previous_track', # Alternative previous
        }
        
        # Desktop Mode Mappings
        self.desktop_mappings = {
            'swipe_up': 'scroll_up',
            'swipe_down': 'scroll_down',
            'swipe_left': 'browser_back',
            'swipe_right': 'browser_forward',
            'open_palm': 'show_desktop',
            'fist': 'minimize_window',
            'peace': 'screenshot',
            'pointing': 'refresh_page',
            'three_fingers': 'new_tab',
            'rock_sign': 'scroll_up',        # 🤘 EASY scroll up!
            'hang_loose': 'scroll_down',     # 🤙 EASY scroll down!
            'three_thumb': 'browser_forward', # Alternative forward
            'four_fingers': 'browser_back',   # Alternative back
        }
        
        # Custom Mode Mappings (User configurable)
        self.custom_mappings = {
            'pointing': 'custom_action_1',
            'thumbs_up': 'custom_action_2',
            'peace': 'custom_action_3'
        }
    
    def set_mode(self, mode):
        """Set current control mode"""
        if isinstance(mode, str):
            mode = ControlMode(mode)
        
        self.current_mode = mode
        self._log_action(f"Mode changed to: {mode.value}")
    
    def execute_gesture(self, gesture_name):
        """Execute action based on gesture and current mode"""
        if not gesture_name:
            return False
        
        # Get action mapping based on current mode
        action = self._get_action_for_gesture(gesture_name)
        
        if action:
            success = self._execute_action(action)
            if success:
                self._log_action(f"Gesture: {gesture_name} -> Action: {action}")
            return success
        
        return False
    
    def _get_action_for_gesture(self, gesture_name):
        """Map gesture to action based on current mode"""
        if self.current_mode == ControlMode.SLIDE_MODE:
            return self.slide_mappings.get(gesture_name)
        elif self.current_mode == ControlMode.MUSIC_MODE:
            return self.music_mappings.get(gesture_name)
        elif self.current_mode == ControlMode.DESKTOP_MODE:
            return self.desktop_mappings.get(gesture_name)
        elif self.current_mode == ControlMode.CUSTOM_MODE:
            return self.custom_mappings.get(gesture_name)
        
        return None
    
    def _execute_action(self, action):
        """Execute the specified action"""
        try:
            # Add delay for better reliability
            import time
            time.sleep(0.1)
            
            # Slide Mode Actions
            if action == 'next_slide':
                pyautogui.press('right')
                print("✓ Pressed RIGHT arrow (Next Slide)")
            elif action == 'previous_slide':
                pyautogui.press('left')
                print("✓ Pressed LEFT arrow (Previous Slide)")
            elif action == 'start_presentation':
                pyautogui.press('f5')
                print("✓ Pressed F5 (Start Presentation)")
            elif action == 'end_presentation':
                pyautogui.press('esc')
                print("✓ Pressed ESC (End Presentation)")
            elif action == 'first_slide':
                pyautogui.hotkey('ctrl', 'home')
                print("✓ Pressed CTRL+HOME (First Slide)")
            elif action == 'last_slide':
                pyautogui.hotkey('ctrl', 'end')
                print("✓ Pressed CTRL+END (Last Slide)")
            elif action == 'laser_pointer':
                pyautogui.hotkey('ctrl', 'l')
                print("✓ Pressed CTRL+L (Laser Pointer)")
            
            # Music Mode Actions
            elif action == 'play_pause':
                pyautogui.press('playpause')
                print("✓ Pressed PLAY/PAUSE")
            elif action == 'next_track':
                pyautogui.press('nexttrack')
                print("✓ Pressed NEXT TRACK")
            elif action == 'previous_track':
                pyautogui.press('prevtrack')
                print("✓ Pressed PREVIOUS TRACK")
            elif action == 'volume_up':
                for _ in range(3):
                    pyautogui.press('volumeup')
                print("✓ Volume UP")
            elif action == 'volume_down':
                for _ in range(3):
                    pyautogui.press('volumedown')
                print("✓ Volume DOWN")
            elif action == 'stop':
                pyautogui.press('stop')
                print("✓ Pressed STOP")
            elif action == 'mute_unmute':
                pyautogui.press('volumemute')
                print("✓ Pressed MUTE/UNMUTE")
            
            # Desktop Mode Actions
            elif action == 'scroll_up':
                pyautogui.scroll(200)  # Increased from scroll_speed * 10
                print("✓ Scrolled UP (fast)")
            elif action == 'scroll_down':
                pyautogui.scroll(-200)  # Increased from -scroll_speed * 10
                print("✓ Scrolled DOWN (fast)")
            elif action == 'browser_back':
                pyautogui.hotkey('alt', 'left')
                print("✓ Browser BACK")
            elif action == 'browser_forward':
                pyautogui.hotkey('alt', 'right')
                print("✓ Browser FORWARD")
            elif action == 'refresh_page':
                pyautogui.press('f5')
                print("✓ Page REFRESH")
            elif action == 'new_tab':
                pyautogui.hotkey('ctrl', 't')
                print("✓ New TAB opened")
            elif action == 'show_desktop':
                if platform.system() == 'Windows':
                    pyautogui.hotkey('win', 'd')
                print("✓ Show Desktop")
            elif action == 'minimize_window':
                if platform.system() == 'Windows':
                    pyautogui.hotkey('alt', 'space')
                    time.sleep(0.1)
                    pyautogui.press('n')
                print("✓ Minimize Window")
            elif action == 'screenshot':
                if platform.system() == 'Windows':
                    pyautogui.hotkey('win', 'shift', 's')
                print("✓ Screenshot Tool")
            
            # Custom Actions
            elif action.startswith('custom_action'):
                self._execute_custom_action(action)
            
            else:
                print(f"❌ Unknown action: {action}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error executing action {action}: {e}")
            return False
    
    def _adjust_volume(self, delta):
        """Adjust system volume"""
        try:
            if platform.system() == 'Windows':
                # Use volume up/down keys
                if delta > 0:
                    for _ in range(abs(delta) // 2):
                        pyautogui.press('volumeup')
                else:
                    for _ in range(abs(delta) // 2):
                        pyautogui.press('volumedown')
            elif platform.system() == 'Darwin':  # macOS
                # Use AppleScript for precise volume control
                script = f"set volume output volume ((output volume of (get volume settings)) + {delta})"
                subprocess.run(['osascript', '-e', script])
            elif platform.system() == 'Linux':
                # Use amixer
                subprocess.run(['amixer', 'set', 'Master', f'{abs(delta)}%{"+" if delta > 0 else "-"}'])
        except:
            pass
    
    def _execute_custom_action(self, action):
        """Execute custom user-defined action"""
        # This can be extended for user-specific actions
        print(f"Custom action triggered: {action}")
        # Example: Open specific application
        # subprocess.Popen(['notepad.exe'])
    
    def _log_action(self, message):
        """Log action to history"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        self.action_history.append(log_entry)
        
        # Keep only recent history
        if len(self.action_history) > self.max_history:
            self.action_history.pop(0)
        
        self.last_action_time = time.time()
    
    def get_action_history(self, count=10):
        """Get recent action history"""
        return self.action_history[-count:]
    
    def clear_history(self):
        """Clear action history"""
        self.action_history.clear()
    
    def get_current_mode(self):
        """Get current control mode"""
        return self.current_mode
    
    def get_available_gestures(self):
        """Get available gestures for current mode"""
        if self.current_mode == ControlMode.SLIDE_MODE:
            return list(self.slide_mappings.keys())
        elif self.current_mode == ControlMode.MUSIC_MODE:
            return list(self.music_mappings.keys())
        elif self.current_mode == ControlMode.DESKTOP_MODE:
            return list(self.desktop_mappings.keys())
        elif self.current_mode == ControlMode.CUSTOM_MODE:
            return list(self.custom_mappings.keys())
        
        return []
    
    def update_custom_mapping(self, gesture, action):
        """Update custom gesture mapping"""
        self.custom_mappings[gesture] = action
        self._log_action(f"Custom mapping updated: {gesture} -> {action}")