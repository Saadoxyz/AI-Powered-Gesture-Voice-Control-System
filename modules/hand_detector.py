import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import time


class HandDetector:
    def __init__(self, config):
        """Initialize Hand Detector with Mediapipe"""
        self.config = config
        
        # Initialize Mediapipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=config['hand_detection']['max_hands'],
            min_detection_confidence=config['hand_detection']['min_detection_confidence'],
            min_tracking_confidence=config['hand_detection']['min_tracking_confidence']
        )
        
        # Smoothing buffers for each landmark
        self.smoothing_factor = config['hand_detection']['smoothing_factor']
        self.landmark_buffers = {}
        self.buffer_size = 5
        
        # FPS calculation
        self.prev_time = 0
        self.fps = 0
        
        # Hand data storage
        self.hands_data = []
        
    def process_frame(self, frame):
        """
        Process video frame and extract hand landmarks
        Returns: processed frame, hands data
        """
        start_time = time.time()
        
        # Convert BGR to RGB for Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        
        # Detect hands
        results = self.hands.process(rgb_frame)
        
        rgb_frame.flags.writeable = True
        frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        
        # Reset hands data
        self.hands_data = []
        
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Get hand label (Left/Right)
                hand_label = results.multi_handedness[hand_idx].classification[0].label
                
                # Extract and process landmarks
                landmarks = self._extract_landmarks(hand_landmarks, frame.shape)
                
                # Smooth landmarks
                smoothed_landmarks = self._smooth_landmarks(landmarks, hand_idx)
                
                # Calculate additional features
                hand_data = {
                    'label': hand_label,
                    'landmarks': smoothed_landmarks,
                    'raw_landmarks': landmarks,
                    'features': self._calculate_features(smoothed_landmarks),
                    'bbox': self._get_bounding_box(smoothed_landmarks, frame.shape)
                }
                
                self.hands_data.append(hand_data)
                
                # Draw landmarks on frame
                if self.config['ui']['show_landmarks']:
                    self._draw_landmarks(frame, hand_landmarks, hand_label)
        
        # Calculate FPS
        self._calculate_fps()
        
        return frame, self.hands_data
    
    def _extract_landmarks(self, hand_landmarks, frame_shape):
        """Extract 21 landmarks with normalized and pixel coordinates"""
        h, w, _ = frame_shape
        landmarks = []
        
        for idx, landmark in enumerate(hand_landmarks.landmark):
            # Normalized coordinates (0-1)
            norm_x = landmark.x
            norm_y = landmark.y
            norm_z = landmark.z
            
            # Pixel coordinates
            px = int(norm_x * w)
            py = int(norm_y * h)
            
            landmarks.append({
                'id': idx,
                'x': norm_x,
                'y': norm_y,
                'z': norm_z,
                'px': px,
                'py': py
            })
        
        return landmarks
    
    def _smooth_landmarks(self, landmarks, hand_idx):
        """Apply exponential moving average smoothing"""
        key = f"hand_{hand_idx}"
        
        if key not in self.landmark_buffers:
            self.landmark_buffers[key] = deque(maxlen=self.buffer_size)
        
        buffer = self.landmark_buffers[key]
        buffer.append(landmarks)
        
        if len(buffer) < 2:
            return landmarks
        
        # Apply smoothing
        smoothed = []
        alpha = self.smoothing_factor
        
        for i in range(21):
            if len(buffer) == 1:
                smoothed.append(landmarks[i])
                continue
            
            prev = buffer[-2][i]
            curr = landmarks[i]
            
            smoothed_point = {
                'id': i,
                'x': alpha * curr['x'] + (1 - alpha) * prev['x'],
                'y': alpha * curr['y'] + (1 - alpha) * prev['y'],
                'z': alpha * curr['z'] + (1 - alpha) * prev['z'],
                'px': int(alpha * curr['px'] + (1 - alpha) * prev['px']),
                'py': int(alpha * curr['py'] + (1 - alpha) * prev['py'])
            }
            smoothed.append(smoothed_point)
        
        return smoothed
    
    def _calculate_features(self, landmarks):
        """Calculate geometric features for gesture recognition"""
        features = {}
        
        # Finger tips: thumb(4), index(8), middle(12), ring(16), pinky(20)
        finger_tips = [4, 8, 12, 16, 20]
        finger_pips = [2, 6, 10, 14, 18]  # Proximal joints
        
        # Calculate which fingers are extended
        extended_fingers = []
        for tip, pip in zip(finger_tips, finger_pips):
            if landmarks[tip]['y'] < landmarks[pip]['y']:  # Tip above pip = extended
                extended_fingers.append(1)
            else:
                extended_fingers.append(0)
        
        features['extended_fingers'] = extended_fingers
        features['fingers_count'] = sum(extended_fingers)
        
        # Palm center (approximate)
        palm_x = np.mean([landmarks[i]['x'] for i in [0, 5, 9, 13, 17]])
        palm_y = np.mean([landmarks[i]['y'] for i in [0, 5, 9, 13, 17]])
        features['palm_center'] = (palm_x, palm_y)
        
        # Hand orientation
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        features['orientation'] = np.arctan2(
            middle_mcp['y'] - wrist['y'],
            middle_mcp['x'] - wrist['x']
        )
        
        # Distances between key points
        features['distances'] = self._calculate_distances(landmarks)
        
        return features
    
    def _calculate_distances(self, landmarks):
        """Calculate distances between key landmarks"""
        distances = {}
        
        # Thumb to index tip
        distances['thumb_index'] = self._euclidean_distance(
            landmarks[4], landmarks[8]
        )
        
        # Thumb to middle tip
        distances['thumb_middle'] = self._euclidean_distance(
            landmarks[4], landmarks[12]
        )
        
        # Index to pinky tip
        distances['index_pinky'] = self._euclidean_distance(
            landmarks[8], landmarks[20]
        )
        
        # Wrist to middle finger tip
        distances['wrist_middle'] = self._euclidean_distance(
            landmarks[0], landmarks[12]
        )
        
        return distances
    
    def _euclidean_distance(self, p1, p2):
        """Calculate Euclidean distance between two points"""
        return np.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)
    
    def _get_bounding_box(self, landmarks, frame_shape):
        """Calculate bounding box around hand"""
        h, w, _ = frame_shape
        
        x_coords = [lm['x'] for lm in landmarks]
        y_coords = [lm['y'] for lm in landmarks]
        
        x_min = int(min(x_coords) * w)
        x_max = int(max(x_coords) * w)
        y_min = int(min(y_coords) * h)
        y_max = int(max(y_coords) * h)
        
        # Add padding
        padding = 20
        x_min = max(0, x_min - padding)
        x_max = min(w, x_max + padding)
        y_min = max(0, y_min - padding)
        y_max = min(h, y_max + padding)
        
        return (x_min, y_min, x_max, y_max)
    
    def _draw_landmarks(self, frame, hand_landmarks, hand_label):
        """Draw hand landmarks and connections on frame"""
        self.mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style()
        )
        
        # Draw hand label
        h, w, _ = frame.shape
        wrist = hand_landmarks.landmark[0]
        cv2.putText(
            frame,
            hand_label,
            (int(wrist.x * w), int(wrist.y * h) - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
    
    def _calculate_fps(self):
        """Calculate and update FPS"""
        current_time = time.time()
        self.fps = 1 / (current_time - self.prev_time) if self.prev_time > 0 else 0
        self.prev_time = current_time
    
    def get_fps(self):
        """Return current FPS"""
        return int(self.fps)
    
    def release(self):
        """Release resources"""
        self.hands.close()