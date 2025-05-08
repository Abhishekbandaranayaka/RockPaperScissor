"""
Gesture Detection Module for Rock Paper Scissors Game
Author: BTMASDB Rathnayaka
Index : 22827
Date: May 08, 2025
Description: This module implements gesture detection logic using MediaPipe to recognize
hand gestures (Rock, Paper, Scissors, Lizard, Spock) from webcam input. It includes
visualization of hand landmarks and supports both RPS and RPSLS game modes.
"""

import cv2  # OpenCV for webcam capture and image processing
import mediapipe as mp  # MediaPipe for hand landmark detection
import numpy as np  # NumPy for numerical operations

# Initialize MediaPipe Hands solution for gesture detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,  # Limit to one hand for simplicity
    min_detection_confidence=0.8,  # Minimum confidence for hand detection
    min_tracking_confidence=0.8  # Minimum confidence for hand tracking
)

def detect_gesture(landmarks, game_mode="RPS"):
    """
    Detect hand gestures based on finger positions.

    Args:
        landmarks (list): List of normalized hand landmarks from MediaPipe.
        game_mode (str): Game mode, either "RPS" or "RPSLS" (default: "RPS").

    Returns:
        str: Detected gesture ("Rock", "Paper", "Scissors", "Lizard", "Spock", or None).
    """
    # Extract key landmarks: tips and MCP (metacarpophalangeal) joints
    thumb_tip = landmarks[4]  # Thumb tip
    thumb_mcp = landmarks[2]  # Thumb MCP joint
    index_tip = landmarks[8]  # Index finger tip
    index_mcp = landmarks[5]  # Index finger MCP joint
    middle_tip = landmarks[12]  # Middle finger tip
    middle_mcp = landmarks[9]  # Middle finger MCP joint
    ring_tip = landmarks[16]  # Ring finger tip
    ring_mcp = landmarks[13]  # Ring finger MCP joint
    pinky_tip = landmarks[20]  # Pinky finger tip
    pinky_mcp = landmarks[17]  # Pinky finger MCP joint

    def is_finger_extended(tip, mcp, threshold=0.05):
        """
        Check if a finger is extended based on tip and MCP joint positions.

        Args:
            tip: Landmark of the finger tip.
            mcp: Landmark of the MCP joint.
            threshold (float): Vertical distance threshold for extension (default: 0.05).

        Returns:
            bool: True if finger is extended, False otherwise.
        """
        return tip.y < mcp.y - threshold  # Finger extended if tip is above MCP

    # Determine finger extension states
    thumb_extended = is_finger_extended(thumb_tip, thumb_mcp)
    index_extended = is_finger_extended(index_tip, index_mcp)
    middle_extended = is_finger_extended(middle_tip, middle_mcp)
    ring_extended = is_finger_extended(ring_tip, ring_mcp)
    pinky_extended = is_finger_extended(pinky_tip, pinky_mcp)

    # Gesture detection logic
    if game_mode == "RPS":
        if not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "Rock"  # All fingers closed
        elif index_extended and middle_extended and ring_extended and pinky_extended:
            return "Paper"  # All fingers extended
        elif index_extended and middle_extended and not ring_extended and not pinky_extended:
            return "Scissors"  # Index and middle extended, others closed
    elif game_mode == "RPSLS":
        if not index_extended and not middle_extended and ring_extended and pinky_extended:
            return "Lizard"  # Ring and pinky extended, others closed
        elif index_extended and middle_extended and not ring_extended and pinky_extended:
            return "Spock"  # Index, middle, and pinky extended, others closed
        # Include RPS gestures for compatibility
        elif not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "Rock"
        elif index_extended and middle_extended and ring_extended and pinky_extended:
            return "Paper"
        elif index_extended and middle_extended and not ring_extended and not pinky_extended:
            return "Scissors"
    return None  # Return None if no gesture is detected

def visualize_landmarks(frame, landmarks):
    """
    Visualize hand landmarks on the input frame.

    Args:
        frame (numpy.ndarray): Input image frame.
        landmarks: Hand landmarks from MediaPipe.

    Returns:
        numpy.ndarray: Frame with drawn landmarks and connections.
    """
    if landmarks:
        contour_img = frame.copy()  # Create a copy to avoid modifying the original
        mp_drawing.draw_landmarks(
            contour_img, landmarks, mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2),  # Landmark points in red
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)   # Connections in green
        )
        return contour_img
    return frame  # Return original frame if no landmarks detected

# Test function to demonstrate gesture detection and visualization
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # Open the default webcam
    if not cap.isOpened():
        print("Error: Could not open webcam.")
    else:
        with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
            print("Starting gesture detection. Show hand gestures (RPSLS mode). Press 'q' to quit.")
            while True:
                ret, frame = cap.read()  # Capture frame from webcam
                if not ret:
                    print("Error: Could not read frame.")
                    break
                frame = cv2.flip(frame, 1)  # Mirror the frame for natural viewing
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for MediaPipe
                results = hands.process(frame_rgb)  # Process frame for hand detection
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        gesture = detect_gesture(hand_landmarks.landmark, "RPSLS")  # Detect gesture
                        print(f"Detected gesture: {gesture}")  # Output detected gesture
                        frame = visualize_landmarks(frame, hand_landmarks)  # Visualize landmarks
                cv2.imshow("Gesture Detection", frame)  # Display the frame
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key
                    break
        cap.release()  # Release the webcam
        cv2.destroyAllWindows()  # Close all OpenCV windows