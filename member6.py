"""
Evidence Recorder Module for Rock Paper Scissors Game
Author: [sadula fernando] (Member 6)
Date: May 08, 2025
Description: This module implements a utility to capture webcam screenshots as evidence
for the Rock Paper Scissors game. Screenshots are saved with timestamps in a designated
directory for documentation purposes.
"""

import cv2  # OpenCV for webcam capture and image saving
import os  # OS module for directory and file operations
import time  # Time module for timestamp generation

class EvidenceRecorder:
    def __init__(self, save_path="report/evidence"):
        """
        Initialize the EvidenceRecorder with a save path for screenshots.

        Args:
            save_path (str): Directory path to save screenshots (default: "report/evidence").
        """
        self.save_path = save_path  # Set the directory path for saving screenshots
        if not os.path.exists(save_path):
            os.makedirs(save_path)  # Create the directory if it doesn't exist
        self.screenshot_count = 0  # Counter for numbering screenshots

    def capture_screenshot(self, frame, prefix="evidence"):
        """
        Capture and save a screenshot from the webcam frame.

        Args:
            frame (numpy.ndarray): The webcam frame to save.
            prefix (str): Prefix for the screenshot filename (default: "evidence").
        """
        timestamp = time.strftime("%Y%m%d-%H%M%S")  # Generate timestamp for unique filename
        filename = f"{prefix}_{self.screenshot_count}_{timestamp}.png"  # Create filename
        filepath = os.path.join(self.save_path, filename)  # Construct full file path
        cv2.imwrite(filepath, frame)  # Save the frame as an image
        print(f"Screenshot saved: {filepath}")  # Confirm save operation
        self.screenshot_count += 1  # Increment screenshot counter

    def run(self):
        """
        Run the evidence recorder to capture screenshots from the webcam.
        Press 's' to capture a screenshot, 'q' to quit.
        """
        cap = cv2.VideoCapture(0)  # Open the default webcam
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return
        print("Press 's' to capture a screenshot, 'q' to quit.")
        while True:
            ret, frame = cap.read()  # Capture frame from webcam
            if not ret:
                print("Error: Could not read frame.")
                break
            frame = cv2.flip(frame, 1)  # Mirror the frame for natural viewing
            cv2.imshow("Evidence Recorder", frame)  # Display the frame
            key = cv2.waitKey(1) & 0xFF  # Capture keypress
            if key == ord('s'):
                self.capture_screenshot(frame, "member6")  # Capture screenshot on 's' key
            elif key == ord('q'):
                break  # Exit on 'q' key
        cap.release()  # Release the webcam
        cv2.destroyAllWindows()  # Close all OpenCV windows

# Test function to demonstrate evidence recording
if __name__ == "__main__":
    recorder = EvidenceRecorder()  # Create an instance of EvidenceRecorder
    recorder.run()  # Start the recording process
