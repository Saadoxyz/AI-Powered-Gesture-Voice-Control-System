"""
Module 2: Gesture Recognition & Classification
Member 2: AI/ML Module
Handles gesture recognition using ML and rule-based logic
"""

import numpy as np
import time
import json
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
from collections import deque
class GestureRecognizer:
    def __init__(self, config):
        """Initialize Gesture Recognizer"""
        self.config = config
        
        # Load gesture definitions
        self.gesture_definitions = self._load_gesture_definitions()
        
        # Gesture history for dynamic gestures
        self.gesture_history = deque(maxlen=15)
        
        # Simple cooldown
        self.last_gesture_time = {}
        self.cooldown = 1.0  # Simple 1 second cooldown for ALL gestures
        
        # ML Model
        self.use_ml = False  # DISABLE ML - use simple rules only
        self.ml_model = None
        self.scaler = None
        
        # Current gesture
        self.current_gesture = None
        self.gesture_confidence = 0.0
        
        # Simple counters
        self.gesture_hold_count = {}  # How many frames gesture is held
        
    def _load_gesture_definitions(self):
        """Load gesture definitions from JSON"""
        gesture_file = 'models/gesture_data.json'
        
        if os.path.exists(gesture_file):
            with open(gesture_file, 'r') as f:
                return json.load(f)
        else:
            # Create default gesture definitions
            default_gestures = {
                "static_gestures": {
                    "open_palm": {
                        "fingers": [1, 1, 1, 1, 1],
                        "description": "All fingers extended"
                    },
                    "fist": {
                        "fingers": [0, 0, 0, 0, 0],
                        "description": "All fingers closed"
                    },
                    "thumbs_up": {
                        "fingers": [1, 0, 0, 0, 0],
                        "description": "Only thumb extended"
                    },
                    "peace": {
                        "fingers": [0, 1, 1, 0, 0],
                        "description": "Index and middle extended"
                    },
                    "pointing": {
                        "fingers": [0, 1, 0, 0, 0],
                        "description": "Only index finger extended"
                    },
                    "ok_sign": {
                        "description": "Thumb and index touching",
                        "special": "thumb_index_close"
                    },
                    "three_fingers": {
                        "fingers": [0, 1, 1, 1, 0],
                        "description": "Three fingers extended"
                    }
                },
                "dynamic_gestures": {
                    "swipe_right": {
                        "type": "horizontal_movement",
                        "direction": "right",
                        "threshold": 0.10
                    },
                    "swipe_left": {
                        "type": "horizontal_movement",
                        "direction": "left",
                        "threshold": 0.10
                    },
                    "swipe_up": {
                        "type": "vertical_movement",
                        "direction": "up",
                        "threshold": 0.10
                    },
                    "swipe_down": {
                        "type": "vertical_movement",
                        "direction": "down",
                        "threshold": 0.10
                    },
                    "pinch_in": {
                        "type": "pinch",
                        "direction": "in"
                    },
                    "pinch_out": {
                        "type": "pinch",
                        "direction": "out"
                    }
                }
            }
            
            # Create models directory if it doesn't exist
            os.makedirs('models', exist_ok=True)
            
            # Save default gestures
            with open(gesture_file, 'w') as f:
                json.dump(default_gestures, f, indent=2)
            
            return default_gestures
    
    def _initialize_ml_model(self):
        """Initialize or load ML model for gesture classification"""
        model_file = 'models/gesture_classifier.pkl'
        
        try:
            if os.path.exists(model_file) and os.path.getsize(model_file) > 0:
                # Load pre-trained model
                with open(model_file, 'rb') as f:
                    data = pickle.load(f)
                    self.ml_model = data['model']
                    self.scaler = data['scaler']
                print("ML model loaded successfully")
            else:
                raise FileNotFoundError("Model file not found or empty")
        except Exception as e:
            print(f"Creating new ML model: {e}")
            # Create and train a basic model with synthetic data
            self.ml_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.scaler = StandardScaler()
            
            # Generate synthetic training data for demonstration
            self._train_basic_model()
    
    def _train_basic_model(self):
        """Train a basic ML model with synthetic data"""
        # Generate synthetic features for common gestures
        X_train = []
        y_train = []
        
        # Open palm (all fingers extended)
        for _ in range(50):
            features = self._generate_synthetic_features([1, 1, 1, 1, 1])
            X_train.append(features)
            y_train.append('open_palm')
        
        # Fist (all fingers closed)
        for _ in range(50):
            features = self._generate_synthetic_features([0, 0, 0, 0, 0])
            X_train.append(features)
            y_train.append('fist')
        
        # Pointing (index finger)
        for _ in range(50):
            features = self._generate_synthetic_features([0, 1, 0, 0, 0])
            X_train.append(features)
            y_train.append('pointing')
        
        # Peace sign
        for _ in range(50):
            features = self._generate_synthetic_features([0, 1, 1, 0, 0])
            X_train.append(features)
            y_train.append('peace')
        
        # Scale and train
        X_train = np.array(X_train)
        self.scaler.fit(X_train)
        X_train_scaled = self.scaler.transform(X_train)
        
        self.ml_model.fit(X_train_scaled, y_train)
        
        # Save model
        model_data = {
            'model': self.ml_model,
            'scaler': self.scaler
        }
        with open('models/gesture_classifier.pkl', 'wb') as f:
            pickle.dump(model_data, f)
    
    def _generate_synthetic_features(self, fingers):
        """Generate synthetic feature vector"""
        features = []
        features.extend(fingers)  # Finger states
        features.append(sum(fingers))  # Count
        
        # Add random variations for realism
        for _ in range(10):
            features.append(np.random.uniform(0, 1))
        
        return features
    
    def recognize_gesture(self, hands_data):
        """
        SIMPLE gesture recognition - RELIABLE
        """
        if not hands_data:
            # Clear history when no hands
            self.gesture_history.clear()
            self.gesture_hold_count.clear()
            return None, 0.0
        
        hand_data = hands_data[0]
        
        # Add to history
        self.gesture_history.append({
            'features': hand_data['features'],
            'landmarks': hand_data['landmarks'],
            'timestamp': time.time()
        })
        
        # STEP 1: Check for STATIC gestures (easier to detect)
        static_gesture, static_conf = self._recognize_static_simple(hand_data)
        
        # STEP 2: Check for SWIPE gestures (only if no static)
        swipe_gesture = None
        swipe_conf = 0.0
        
        if not static_gesture:
            swipe_gesture, swipe_conf = self._recognize_swipe_simple()
        
        # Pick the best one
        if static_conf > swipe_conf:
            gesture = static_gesture
            confidence = static_conf
        else:
            gesture = swipe_gesture
            confidence = swipe_conf
        
        # Check cooldown
        if gesture and self._check_cooldown_simple(gesture):
            self.current_gesture = gesture
            self.gesture_confidence = confidence
            self.last_gesture_time[gesture] = time.time()
            
            # Clear history after gesture detected
            self.gesture_history.clear()
            
            return gesture, confidence
        
        return None, 0.0
    
    def _recognize_static_simple(self, hand_data):
        """SIMPLE static gesture recognition with ALTERNATIVES"""
        features = hand_data['features']
        fingers = features['extended_fingers']
        count = sum(fingers)
        
        # Count how many frames this pattern is held
        pattern_key = str(fingers)
        if pattern_key not in self.gesture_hold_count:
            self.gesture_hold_count[pattern_key] = 0
        
        self.gesture_hold_count[pattern_key] += 1
        
        # Clear other patterns
        for key in list(self.gesture_hold_count.keys()):
            if key != pattern_key:
                self.gesture_hold_count[key] = 0
        
        # Need to hold for 5 frames (about 0.15 seconds)
        if self.gesture_hold_count[pattern_key] < 5:
            return None, 0.0
        
        # ===== BASIC GESTURES (Keep as is) =====
        
        # All 5 fingers open = OPEN PALM
        if fingers == [1, 1, 1, 1, 1]:
            return 'open_palm', 0.95
        
        # All fingers closed = FIST
        if fingers == [0, 0, 0, 0, 0]:
            return 'fist', 0.95
        
        # Only index finger = POINTING
        if fingers == [0, 1, 0, 0, 0]:
            return 'pointing', 0.95
        
        # Index + Middle = PEACE
        if fingers == [0, 1, 1, 0, 0]:
            return 'peace', 0.95
        
        # Only thumb = THUMBS UP
        if fingers == [1, 0, 0, 0, 0]:
            return 'thumbs_up', 0.95
        
        # ===== NEW ALTERNATIVE GESTURES =====
        
        # 🤘 ROCK (Index + Pinky) = VOLUME UP / SCROLL UP
        if fingers == [0, 1, 0, 0, 1]:
            return 'rock_sign', 0.95
        
        # 🤙 HANG LOOSE (Thumb + Pinky) = VOLUME DOWN / SCROLL DOWN
        if fingers == [1, 0, 0, 0, 1]:
            return 'hang_loose', 0.95
        
        # 👌 OK SIGN simulation (Thumb + Index + Middle) = NEXT
        if fingers == [1, 1, 1, 0, 0]:
            return 'three_thumb', 0.95
        
        # 🖖 VULCAN (Middle + Ring split) = PREVIOUS
        if fingers == [0, 1, 1, 1, 1]:
            return 'four_fingers', 0.95
        
        # Three fingers (Index + Middle + Ring) = GENERAL ACTION
        if fingers == [0, 1, 1, 1, 0]:
            return 'three_fingers', 0.95
        
        return None, 0.0
    
    def _recognize_swipe_simple(self):
        """EASIER swipe recognition - MORE FLEXIBLE"""
        if len(self.gesture_history) < 6:  # Reduced from 8 - faster detection
            return None, 0.0
        
        # Get positions
        positions = [entry['features']['palm_center'] for entry in list(self.gesture_history)[-6:]]
        
        # Movement from start to end
        start = positions[0]
        end = positions[-1]
        
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        
        # EASIER threshold - only need 10% movement
        move_size = np.sqrt(dx**2 + dy**2)
        
        if move_size < 0.10:  # Reduced from 0.15
            return None, 0.0
        
        # MORE FLEXIBLE direction detection
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        
        # HORIZONTAL swipe - dx must be 2x bigger (was 3x)
        if abs_dx > abs_dy * 2:
            if dx > 0:
                return 'swipe_right', 0.90
            else:
                return 'swipe_left', 0.90
        
        # VERTICAL swipe - dy must be 2x bigger (was 3x)
        if abs_dy > abs_dx * 2:
            if dy > 0:
                return 'swipe_down', 0.90
            else:
                return 'swipe_up', 0.90
        
        # Not clear enough
        return None, 0.0
    
    def _check_cooldown_simple(self, gesture):
        """Smart cooldown - shorter for swipes"""
        if gesture in self.last_gesture_time:
            elapsed = time.time() - self.last_gesture_time[gesture]
            
            # Swipes can be faster
            if gesture.startswith('swipe'):
                return elapsed > 0.6  # Only 0.6 seconds for swipes
            else:
                return elapsed > 1.0  # 1 second for static gestures
        return True
        """Recognize static hand gestures - BALANCED"""
        features = hand_data['features']
        extended_fingers = features['extended_fingers']
        distances = features['distances']
        
        confidence_threshold = 0.70
        
        # Rule-based recognition
        static_gestures = self.gesture_definitions['static_gestures']
        
        # Check each defined gesture - EXACT MATCH preferred
        for gesture_name, gesture_def in static_gestures.items():
            if 'fingers' in gesture_def:
                # Exact match gets highest confidence
                if extended_fingers == gesture_def['fingers']:
                    confidence = 0.95
                    
                    # Add stability check
                    if gesture_name not in self.gesture_stable_count:
                        self.gesture_stable_count[gesture_name] = 0
                    
                    self.gesture_stable_count[gesture_name] += 1
                    
                    # Need gesture stable for 3 frames
                    if self.gesture_stable_count[gesture_name] >= 3:
                        # Reset other counters
                        for key in list(self.gesture_stable_count.keys()):
                            if key != gesture_name:
                                self.gesture_stable_count[key] = 0
                        
                        return gesture_name, confidence
        
        # Special gestures
        if distances['thumb_index'] < 0.05:
            return 'ok_sign', 0.88
        
        if distances['thumb_middle'] < 0.06:
            return 'pinch', 0.85
        
        # Reset stability counters if no gesture
        self.gesture_stable_count.clear()
        
        return None, 0.0
    
    def _ml_classify(self, hand_data):
        """Classify gesture using ML model"""
        try:
            # Extract features
            features = self._extract_ml_features(hand_data)
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Predict
            prediction = self.ml_model.predict(features_scaled)[0]
            probabilities = self.ml_model.predict_proba(features_scaled)[0]
            confidence = np.max(probabilities)
            
            return prediction, confidence
        except:
            return None, 0.0
    
    def _extract_ml_features(self, hand_data):
        """Extract feature vector for ML model"""
        features = []
        
        # Add finger states
        features.extend(hand_data['features']['extended_fingers'])
        
        # Add finger count
        features.append(hand_data['features']['fingers_count'])
        
        # Add distances
        for dist in hand_data['features']['distances'].values():
            features.append(dist)
        
        # Add palm center
        features.extend(hand_data['features']['palm_center'])
        
        # Add orientation
        features.append(hand_data['features']['orientation'])
        
        # Pad to fixed size
        while len(features) < 15:
            features.append(0.0)
        
        return features[:15]
    
    def _recognize_dynamic_gesture(self):
        """Recognize dynamic gestures - BALANCED and CLEAR"""
        if len(self.gesture_history) < 10:
            return None, 0.0
        
        # Get recent positions
        recent_positions = []
        for entry in list(self.gesture_history)[-10:]:
            palm = entry['features']['palm_center']
            recent_positions.append(palm)
        
        # Calculate movement vector
        start_pos = recent_positions[0]
        end_pos = recent_positions[-1]
        
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        movement_magnitude = np.sqrt(dx**2 + dy**2)
        
        # MODERATE threshold - not too easy, not too hard
        threshold = 0.12
        
        if movement_magnitude < threshold:
            return None, 0.0
        
        confidence = min(movement_magnitude / threshold, 1.0) * 0.90
        
        # CLEAR direction detection - need STRONG dominance
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        
        # If movements are similar, IGNORE (too ambiguous)
        if abs(abs_dx - abs_dy) < 0.05:
            return None, 0.0
        
        # HORIZONTAL must be 2x stronger than vertical
        if abs_dx > abs_dy * 2.0:
            if dx > 0:
                return 'swipe_right', confidence
            else:
                return 'swipe_left', confidence
        
        # VERTICAL must be 2x stronger than horizontal
        elif abs_dy > abs_dx * 2.0:
            if dy > 0:
                return 'swipe_down', confidence
            else:
                return 'swipe_up', confidence
        
        # Not clear enough - ignore
        return None, 0.0
    
    def _check_cooldown(self, gesture):
        """Check if gesture is in cooldown period - BALANCED"""
        if gesture in self.last_gesture_time:
            elapsed = time.time() - self.last_gesture_time[gesture]
            
            # Different cooldowns for different gesture types
            if gesture.startswith('swipe'):
                # Swipes need medium cooldown to prevent spam
                required_cooldown = 0.8
            else:
                # Static gestures need longer cooldown
                required_cooldown = 1.0
            
            return elapsed > required_cooldown
        return True
    
    def get_current_gesture(self):
        """Get current recognized gesture"""
        return self.current_gesture, self.gesture_confidence
    
    def reset_gesture_history(self):
        """Reset gesture history"""
        self.gesture_history.clear()
        self.trajectory_buffer.clear()