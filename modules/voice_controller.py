"""
Module 4: Advanced Voice Recognition & Control
Member 4: Complete Voice Assistant with Browser Control
"""

import speech_recognition as sr
import pyttsx3
import pyautogui
import subprocess
import platform
import time
import webbrowser
import os
from threading import Thread
import json


class VoiceController:
    """Advanced voice assistant with browser automation"""
    
    def __init__(self, config):
        """Initialize advanced voice controller"""
        self.config = config
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Voice is active
        self.is_listening = False
        
        # Context memory
        self.context = {
            'last_contact': None,
            'last_search': None,
            'current_app': None,
            'browser_open': False,
            'search_results_visible': False
        }
        
        # WhatsApp contacts (with multiple name variations)
        self.contacts = {
            'abdul': 'Abdul Rahman',
            'abdul rahman': 'Abdul Rahman',
            'abdur': 'Abdul Rahman',
            'abdur rehman': 'Abdul Rahman',
            'ahmed': 'Ahmed',
            'ali': 'Ali',
            'sara': 'Sara',
            'fatima': 'Fatima',
            'hassan': 'Hassan',
            'zainab': 'Zainab',
            # Add your contacts
        }
        
        # Browser shortcuts
        pyautogui.PAUSE = 0.3  # Pause between actions
        
        print("✓ Advanced Voice Controller initialized")
    
    def speak(self, text):
        """Text to speech"""
        print(f"🔊 Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice command"""
        with self.microphone as source:
            print("🎤 Listening...")
            
            # Adjust for noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"✓ You said: {command}")
                return command
                
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("❌ Could not understand")
                return None
            except sr.RequestError as e:
                print(f"❌ Error: {e}")
                return None
    
    def process_command(self, command):
        """Process and execute voice command"""
        if not command:
            return
        
        command = command.lower()
        
        # ===== GOOGLE & SEARCH =====
        if 'open google' in command or 'google' in command and 'open' in command:
            self._open_google()
        
        elif 'search for' in command or 'search' in command:
            self._handle_search(command)
        
        # ===== CLICK ACTIONS =====
        elif 'click' in command:
            self._handle_click(command)
        
        # ===== YOUTUBE =====
        elif 'youtube' in command or 'video' in command:
            self._handle_youtube(command)
        
        # ===== WHATSAPP / MESSAGING =====
        elif 'whatsapp' in command or 'message' in command or 'mail' in command:
            self._handle_whatsapp(command)
        
        # ===== OPEN APPLICATIONS =====
        elif 'open' in command:
            self._handle_open(command)
        
        # ===== TYPING =====
        elif 'type' in command or 'write' in command:
            self._handle_type(command)
        
        # ===== KEYBOARD ACTIONS =====
        elif 'press' in command or 'enter' in command or 'backspace' in command:
            self._handle_keyboard(command)
        
        # ===== MEDIA CONTROL =====
        elif any(word in command for word in ['play', 'pause', 'volume', 'next', 'previous', 'mute']):
            self._handle_media(command)
        
        # ===== SCROLLING =====
        elif 'scroll' in command:
            self._handle_scroll(command)
        
        # ===== CLOSE/BACK =====
        elif 'go back' in command or 'back' in command:
            self._go_back()
        
        elif 'close' in command or 'exit' in command:
            self._handle_close(command)
        
        # ===== TAKE SCREENSHOT =====
        elif 'screenshot' in command or 'capture' in command:
            self._take_screenshot()
        
        # ===== SYSTEM COMMANDS =====
        elif 'lock screen' in command or 'lock' in command:
            self._lock_screen()
        
        elif 'sleep' in command or 'hibernate' in command:
            self._sleep_system()
        
        elif 'refresh' in command or 'reload' in command:
            self._refresh_page()
        
        elif 'minimize' in command:
            self._minimize_window()
        
        elif 'maximize' in command or 'full screen' in command:
            self._maximize_window()
        
        # ===== STOP LISTENING =====
        elif 'stop listening' in command or 'stop voice' in command or 'exit voice' in command:
            self.speak("Voice control stopped")
            self.is_listening = False
        
        else:
            self.speak("Sorry, I didn't understand that")
    
    # ========== GOOGLE & SEARCH ==========
    
    def _open_google(self):
        """Open Google in browser"""
        self.speak("Opening Google")
        webbrowser.open('https://www.google.com')
        time.sleep(2)
        self.context['browser_open'] = True
        self.context['current_app'] = 'Google'
    
    def _handle_search(self, command):
        """Handle search commands"""
        # Extract search query
        if 'search for' in command:
            query = command.split('search for')[-1].strip()
        elif 'search' in command:
            query = command.replace('search', '').strip()
        else:
            self.speak("What should I search for?")
            query = self.listen()
        
        if not query:
            return
        
        self.context['last_search'] = query
        
        # If browser is open, use search box
        if self.context['browser_open']:
            self.speak(f"Searching for {query}")
            
            # Click search box (Ctrl+L for address bar)
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.5)
            
            # Type search query
            pyautogui.write(query, interval=0.05)
            time.sleep(0.5)
            
            # Press Enter
            pyautogui.press('enter')
            time.sleep(2)
            
            self.context['search_results_visible'] = True
            self.speak("Search complete. You can say click first, second, or third result")
        
        else:
            # Open Google and search
            self.speak(f"Opening Google and searching for {query}")
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            time.sleep(2)
            self.context['browser_open'] = True
            self.context['search_results_visible'] = True
            self.speak("You can say click first, second, or third result")
    
    # ========== CLICK ACTIONS ==========
    
    def _handle_click(self, command):
        """Handle click commands"""
        
        # Click on search results
        if 'first' in command:
            self._click_search_result(1)
        elif 'second' in command or '2nd' in command:
            self._click_search_result(2)
        elif 'third' in command or '3rd' in command:
            self._click_search_result(3)
        elif 'fourth' in command or '4th' in command:
            self._click_search_result(4)
        elif 'fifth' in command or '5th' in command:
            self._click_search_result(5)
        
        # Click video (YouTube)
        elif 'video' in command:
            if 'first' in command:
                self._click_youtube_video(1)
            elif 'second' in command:
                self._click_youtube_video(2)
            elif 'third' in command:
                self._click_youtube_video(3)
        
        else:
            self.speak("Which result should I click?")
    
    def _click_search_result(self, position):
        """Click on Google search result"""
        self.speak(f"Clicking result number {position}")
        
        # Wait for page to load
        time.sleep(1)
        
        # Press Tab to navigate
        for i in range(position + 2):  # Skip Google logo and search box
            pyautogui.press('tab')
            time.sleep(0.2)
        
        # Press Enter to click
        pyautogui.press('enter')
        time.sleep(2)
        
        self.speak("Page opened")
    
    def _click_youtube_video(self, position):
        """Click YouTube video"""
        self.speak(f"Playing video number {position}")
        
        time.sleep(1)
        
        # YouTube videos are usually visible
        # Tab through results
        for i in range(position + 5):  # Skip header elements
            pyautogui.press('tab')
            time.sleep(0.2)
        
        pyautogui.press('enter')
        time.sleep(2)
        
        self.speak("Video playing")
    
    # ========== YOUTUBE ==========
    
    def _handle_youtube(self, command):
        """Handle YouTube commands"""
        
        # Open YouTube
        if 'open youtube' in command:
            self.speak("Opening YouTube")
            webbrowser.open('https://www.youtube.com')
            time.sleep(2)
            self.context['browser_open'] = True
            self.context['current_app'] = 'YouTube'
            self.speak("YouTube is open. What should I search for?")
        
        # Search on YouTube
        elif 'search for' in command or 'search' in command:
            query = command.split('search for')[-1].strip() if 'search for' in command else command.replace('search', '').replace('youtube', '').strip()
            
            if not query:
                self.speak("What should I search for on YouTube?")
                query = self.listen()
            
            if query:
                self.speak(f"Searching YouTube for {query}")
                
                # Click search box
                pyautogui.hotkey('ctrl', 'l')
                time.sleep(0.5)
                
                # If not on YouTube, go there first
                if 'youtube.com' not in command:
                    pyautogui.write('youtube.com', interval=0.05)
                    pyautogui.press('enter')
                    time.sleep(2)
                
                # Click search box on YouTube
                pyautogui.press('/')  # YouTube shortcut for search
                time.sleep(0.5)
                
                # Type search
                pyautogui.write(query, interval=0.05)
                time.sleep(0.5)
                
                # Search
                pyautogui.press('enter')
                time.sleep(2)
                
                self.speak("Search complete. You can say click first video, second video, or third video")
        
        else:
            self.speak("Opening YouTube")
            webbrowser.open('https://www.youtube.com')
            time.sleep(2)
    
    # ========== WHATSAPP ==========
    
    def _handle_whatsapp(self, command):
        """Handle WhatsApp commands"""
        
        # Find contact name
        contact_name = None
        for name, actual_name in self.contacts.items():
            if name in command:
                contact_name = actual_name
                break
        
        if contact_name:
            self.speak(f"Searching for {contact_name}")
            
            # Make sure WhatsApp Web is open
            webbrowser.open('https://web.whatsapp.com')
            time.sleep(2)
            
            # Click on the search box in WhatsApp (it's at the top)
            # Press Ctrl+F to focus search
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            
            # Clear any existing text
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            
            # Type contact name
            pyautogui.write(contact_name, interval=0.05)
            time.sleep(1)
            
            # Press Enter or click first result
            pyautogui.press('enter')
            time.sleep(1.5)
            
            # Ask for message
            self.speak(f"Message for {contact_name}?")
            message = self.listen()
            
            if message:
                # Click in message box and type
                pyautogui.write(message, interval=0.04)
                time.sleep(0.5)
                pyautogui.press('enter')
                self.speak(f"Message sent to {contact_name}")
            else:
                self.speak("No message to send")
        
        elif 'open whatsapp' in command:
            self.speak("Opening WhatsApp")
            webbrowser.open('https://web.whatsapp.com')
            time.sleep(2)
        
        else:
            self.speak("Who should I message?")
            contact_response = self.listen()
            if contact_response:
                # Try to find contact
                for name, actual_name in self.contacts.items():
                    if name in contact_response:
                        contact_name = actual_name
                        self.speak(f"Messaging {contact_name}")
                        
                        webbrowser.open('https://web.whatsapp.com')
                        time.sleep(2)
                        
                        pyautogui.hotkey('ctrl', 'f')
                        time.sleep(0.5)
                        pyautogui.hotkey('ctrl', 'a')
                        pyautogui.write(contact_name, interval=0.05)
                        time.sleep(1)
                        pyautogui.press('enter')
                        time.sleep(1.5)
                        
                        self.speak(f"Message for {contact_name}?")
                        message = self.listen()
                        if message:
                            pyautogui.write(message, interval=0.04)
                            time.sleep(0.5)
                            pyautogui.press('enter')
                            self.speak(f"Message sent to {contact_name}")
                        break

    
    # ========== APPLICATIONS ==========
    
    def _handle_open(self, command):
        """Open applications"""
        
        if 'chrome' in command or 'browser' in command:
            self.speak("Opening Chrome")
            webbrowser.open('https://www.google.com')
            self.context['browser_open'] = True
        
        elif 'notepad' in command:
            self.speak("Opening Notepad")
            if platform.system() == 'Windows':
                subprocess.Popen(['notepad.exe'])
        
        elif 'calculator' in command:
            self.speak("Opening Calculator")
            if platform.system() == 'Windows':
                subprocess.Popen(['calc.exe'])
        
        elif 'file explorer' in command or 'explorer' in command:
            self.speak("Opening File Explorer")
            if platform.system() == 'Windows':
                subprocess.Popen(['explorer.exe'])
        
        else:
            self.speak("I don't know how to open that")
    
    # ========== TYPING ==========
    
    def _handle_type(self, command):
        """Handle typing"""
        text = command.replace('type', '').replace('write', '').strip()
        
        if not text:
            self.speak("What should I type?")
            text = self.listen()
        
        if text:
            pyautogui.write(text, interval=0.05)
            self.speak("Done typing")
    
    # ========== KEYBOARD ==========
    
    def _handle_keyboard(self, command):
        """Handle keyboard actions"""
        
        if 'enter' in command:
            pyautogui.press('enter')
            self.speak("Pressed Enter")
        elif 'backspace' in command or 'delete' in command:
            pyautogui.press('backspace')
        elif 'space' in command:
            pyautogui.press('space')
        elif 'tab' in command:
            pyautogui.press('tab')
        elif 'escape' in command:
            pyautogui.press('esc')
    
    # ========== MEDIA ==========
    
    def _handle_media(self, command):
        """Media controls"""
        
        if 'play' in command:
            pyautogui.press('playpause')
            self.speak("Playing")
        elif 'pause' in command:
            pyautogui.press('playpause')
            self.speak("Paused")
        elif 'volume up' in command:
            for _ in range(3):
                pyautogui.press('volumeup')
            self.speak("Volume up")
        elif 'volume down' in command:
            for _ in range(3):
                pyautogui.press('volumedown')
            self.speak("Volume down")
        elif 'next' in command:
            pyautogui.press('nexttrack')
            self.speak("Next")
        elif 'previous' in command:
            pyautogui.press('prevtrack')
            self.speak("Previous")
    
    # ========== NAVIGATION ==========
    
    def _handle_scroll(self, command):
        """Handle scrolling"""
        
        if 'up' in command:
            pyautogui.scroll(300)
            self.speak("Scrolling up")
        elif 'down' in command:
            pyautogui.scroll(-300)
            self.speak("Scrolling down")
    
    def _go_back(self):
        """Go back in browser"""
        self.speak("Going back")
        pyautogui.hotkey('alt', 'left')
        time.sleep(1)
    
    def _handle_close(self, command):
        """Close window/tab"""
        
        if 'tab' in command:
            self.speak("Closing tab")
            pyautogui.hotkey('ctrl', 'w')
        elif 'window' in command:
            self.speak("Closing window")
            pyautogui.hotkey('alt', 'f4')
    
    # ========== SCREENSHOT ==========
    
    def _take_screenshot(self):
        """Take screenshot"""
        import pyautogui
        self.speak("Taking screenshot")
        pyautogui.hotkey('printscreen')
        time.sleep(0.5)
        self.speak("Screenshot captured")
    
    # ========== SYSTEM CONTROL ==========
    
    def _lock_screen(self):
        """Lock the screen"""
        self.speak("Locking screen")
        if platform.system() == 'Windows':
            subprocess.Popen(['rundll32.exe', 'user32.dll,LockWorkStation'])
    
    def _sleep_system(self):
        """Put system to sleep"""
        self.speak("Going to sleep")
        if platform.system() == 'Windows':
            subprocess.Popen(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0', '1', '0'])
    
    def _refresh_page(self):
        """Refresh page"""
        self.speak("Refreshing page")
        pyautogui.press('f5')
        time.sleep(1)
    
    def _minimize_window(self):
        """Minimize window"""
        self.speak("Minimizing window")
        pyautogui.hotkey('super', 'd')
    
    def _maximize_window(self):
        """Maximize window"""
        self.speak("Maximizing window")
        pyautogui.hotkey('super', 'up')
    
    # ========== LISTENING LOOP ==========
    
    def start_listening_loop(self):
        """Continuous listening"""
        self.is_listening = True
        self.speak("Voice assistant activated. I'm ready to help")
        
        while self.is_listening:
            command = self.listen()
            if command:
                self.process_command(command)
            time.sleep(0.3)
    
    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False