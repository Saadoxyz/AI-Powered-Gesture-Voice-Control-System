
import numpy as np
import cv2


def normalize_landmarks(landmarks, width, height):
    """
    Normalize landmark coordinates to 0-1 range
    """
    normalized = []
    for landmark in landmarks:
        norm_landmark = {
            'x': landmark['px'] / width,
            'y': landmark['py'] / height,
            'z': landmark['z']
        }
        normalized.append(norm_landmark)
    return normalized


def calculate_angle(p1, p2, p3):
    """
    Calculate angle between three points
    Args:
        p1, p2, p3: Points as dicts with 'x', 'y' keys
    Returns:
        Angle in degrees
    """
    radians = np.arctan2(p3['y'] - p2['y'], p3['x'] - p2['x']) - \
              np.arctan2(p1['y'] - p2['y'], p1['x'] - p2['x'])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle


def smooth_value(current, previous, alpha=0.5):
    """
    Apply exponential moving average smoothing
    Args:
        current: Current value
        previous: Previous smoothed value
        alpha: Smoothing factor (0-1)
    Returns:
        Smoothed value
    """
    if previous is None:
        return current
    return alpha * current + (1 - alpha) * previous


def detect_hand_orientation(landmarks):
    """
    Detect if hand is facing camera or away
    Returns: 'front' or 'back'
    """
    # Use z-coordinates to determine orientation
    wrist_z = landmarks[0]['z']
    fingertip_z = np.mean([landmarks[i]['z'] for i in [4, 8, 12, 16, 20]])
    
    if fingertip_z < wrist_z:
        return 'front'  # Palm facing camera
    else:
        return 'back'   # Back of hand facing camera


def get_hand_bounding_box(landmarks, padding=20):
    """
    Calculate bounding box around hand with padding
    """
    x_coords = [lm['px'] for lm in landmarks]
    y_coords = [lm['py'] for lm in landmarks]
    
    x_min = max(0, min(x_coords) - padding)
    x_max = max(x_coords) + padding
    y_min = max(0, min(y_coords) - padding)
    y_max = max(y_coords) + padding
    
    return (int(x_min), int(y_min), int(x_max), int(y_max))


def enhance_frame(frame):
    """
    Enhance video frame for better detection
    """
    # Increase brightness slightly
    enhanced = cv2.convertScaleAbs(frame, alpha=1.1, beta=10)
    
    # Apply slight sharpening
    kernel = np.array([[-1,-1,-1],
                       [-1, 9,-1],
                       [-1,-1,-1]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    
    return sharpened


def draw_info_overlay(frame, fps, gesture, confidence, mode):
    """
    Draw information overlay on frame
    """
    h, w = frame.shape[:2]
    
    # Semi-transparent overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (300, 120), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
    
    # Text information
    info_text = [
        f"FPS: {fps}",
        f"Mode: {mode}",
        f"Gesture: {gesture if gesture else 'None'}",
        f"Confidence: {int(confidence * 100)}%"
    ]
    
    y_offset = 30
    for text in info_text:
        cv2.putText(frame, text, (20, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        y_offset += 25
    
    return frame


def calculate_distance_3d(p1, p2):
    """
    Calculate 3D Euclidean distance between two points
    """
    return np.sqrt(
        (p1['x'] - p2['x'])**2 +
        (p1['y'] - p2['y'])**2 +
        (p1['z'] - p2['z'])**2
    )


def is_finger_extended(landmarks, finger_idx):
    """
    Check if a specific finger is extended
    Args:
        landmarks: List of hand landmarks
        finger_idx: 0=thumb, 1=index, 2=middle, 3=ring, 4=pinky
    Returns:
        Boolean indicating if finger is extended
    """
    # Finger tip and PIP joint indices
    finger_tips = [4, 8, 12, 16, 20]
    finger_pips = [2, 6, 10, 14, 18]
    
    tip_idx = finger_tips[finger_idx]
    pip_idx = finger_pips[finger_idx]
    
    # For thumb, check x-coordinate instead
    if finger_idx == 0:
        return abs(landmarks[tip_idx]['x'] - landmarks[2]['x']) > 0.05
    
    # For other fingers, compare y-coordinates
    return landmarks[tip_idx]['y'] < landmarks[pip_idx]['y']