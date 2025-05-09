"""
Rock Paper Scissors Game with Enhanced GUI, Speech Recognition, and Screenshot Saving
Authors: BTMASDB Rathnayaka / Kavidu Nimantha / Imalshika Herath / Udeshi Wijesekara / Gayathri Konara / sadula fernando
Date: May 08, 2025
Description: This script integrates gesture detection, image processing, game logic,
speech recognition, and screenshot saving into a user-friendly Rock Paper Scissors game.
It features a beautiful GUI. Speech recognition allows voice commands like "start,"
"proceed," and "reset." Screenshots are saved at game end.
"""

import cv2  # OpenCV for webcam capture and image processing
import mediapipe as mp  # MediaPipe for hand gesture detection
import numpy as np  # NumPy for numerical operations
import tkinter as tk  # Tkinter for GUI creation
from PIL import Image, ImageTk  # Pillow for image handling in Tkinter
import random  # Random for AI choice generation
import time  # Time for timestamp generation
from tkinter import ttk  # Tkinter themed widgets for table display
import speech_recognition as sr  # Speech recognition library
import threading  # Threading for non-blocking speech recognition
import os  # OS for file operations

# Initialize MediaPipe Hands for gesture detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Initialize Speech Recognizer
recognizer = sr.Recognizer()

class GameLogic:

def detect_gesture(landmarks, game_mode="RPS"):
    """
    Detect hand gestures based on finger positions.

    Args:
        landmarks (list): List of hand landmarks from MediaPipe.
        game_mode (str): Game mode (default: "RPS").

    Returns:
        str: Detected gesture or None.
    """
    thumb_tip = landmarks[4]
    thumb_mcp = landmarks[2]
    index_tip = landmarks[8]
    index_mcp = landmarks[5]
    middle_tip = landmarks[12]
    middle_mcp = landmarks[9]
    ring_tip = landmarks[16]
    ring_mcp = landmarks[13]
    pinky_tip = landmarks[20]
    pinky_mcp = landmarks[17]

    def is_finger_extended(tip, mcp, threshold=0.05):
        return tip.y < mcp.y - threshold

    thumb_extended = is_finger_extended(thumb_tip, thumb_mcp)
    index_extended = is_finger_extended(index_tip, index_mcp)
    middle_extended = is_finger_extended(middle_tip, middle_mcp)
    ring_extended = is_finger_extended(ring_tip, ring_mcp)
    pinky_extended = is_finger_extended(pinky_tip, pinky_mcp)

    if game_mode == "RPS":
        if not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "Rock"
        elif index_extended and middle_extended and ring_extended and pinky_extended:
            return "Paper"
        elif index_extended and middle_extended and not ring_extended and not pinky_extended:
            return "Scissors"
    elif game_mode == "RPSLS":
        if not index_extended and not middle_extended and ring_extended and pinky_extended:
            return "Lizard"
        elif index_extended and middle_extended and not ring_extended and pinky_extended:
            return "Spock"
        elif not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "Rock"
        elif index_extended and middle_extended and ring_extended and pinky_extended:
            return "Paper"
        elif index_extended and middle_extended and not ring_extended and not pinky_extended:
            return "Scissors"
    return None

class GUIDemo:    

        def show_preview(self):
        """Display live preview on panels until Proceed button is clicked."""
        if not self.game_active:
            return
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame.")
            self.result_label.config(text="Error: Could not read frame. Restart the game.")
            return
        frame = cv2.flip(frame, 1)
        grey, thresh, bg_removed = process_image(frame)
        self.update_image(self.webcam_label, frame)
        self.update_image(self.grey_label, grey)
        self.update_image(self.thresh_label, thresh)
        self.update_image(self.bg_label, bg_removed)
        if not self.showing_preview and time.time() - self.preview_start_time > 1.0:  # Wait 1 second for stability
            self.result_label.config(text=f"Panels active. Say 'proceed' or click 'Proceed to Round {self.round_number + 1}'...")
            self.showing_preview = True
        # Schedule the next preview update with a longer interval
        self.preview_after_id = self.root.after(50, self.show_preview)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = GUIDemo(root)
    root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    root.mainloop()