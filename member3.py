"""
GUI Display Module for Rock Paper Scissors Game
Author: Imalshika Herath
Index Number : 22857
Date: May 08, 2025
Description: This module implements a Tkinter-based GUI for the Rock Paper Scissors game,
displaying the webcam feed, processed images (greyscale, thresholded, background removed),
and game results. It integrates image processing to visualize each stage.
"""

import tkinter as tk  # Tkinter for GUI creation
from PIL import Image, ImageTk  # Pillow for image handling in Tkinter
import cv2  # OpenCV for webcam capture and image processing
import numpy as np  # NumPy for numerical operations and array handling

class GUIDemo:
    def __init__(self, root):
        """
        Initialize the GUI with panels for webcam feed, processed images, and results.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Rock Paper Scissors GUI")  # Set window title
        self.root.geometry("1200x600")  # Set window size to accommodate all panels
        self.root.configure(bg="#f0f0f0")  # Light grey background for visual appeal

        # Create a frame to hold image panels
        panel_frame = tk.Frame(self.root, bg="#f0f0f0")
        panel_frame.pack(pady=10)

        # Webcam Feed panel
        tk.Label(panel_frame, text="Webcam Feed", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        self.webcam_label = tk.Label(panel_frame, bg="#ffffff", borderwidth=2, relief="solid")
        self.webcam_label.pack(side=tk.LEFT, padx=10)

        # Greyscale panel
        tk.Label(panel_frame, text="Greyscale", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        self.grey_label = tk.Label(panel_frame, bg="#ffffff", borderwidth=2, relief="solid")
        self.grey_label.pack(side=tk.LEFT, padx=10)

        # Thresholded panel
        tk.Label(panel_frame, text="Thresholded", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        self.thresh_label = tk.Label(panel_frame, bg="#ffffff", borderwidth=2, relief="solid")
        self.thresh_label.pack(side=tk.LEFT, padx=10)

        # Background Removed panel
        tk.Label(panel_frame, text="Background Removed", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        self.bg_label = tk.Label(panel_frame, bg="#ffffff", borderwidth=2, relief="solid")
        self.bg_label.pack(side=tk.LEFT, padx=10)

        # Result display label
        self.result_label = tk.Label(self.root, text="Result: None", font=("Arial", 14), fg="#ff0000", bg="#f0f0f0")
        self.result_label.pack(pady=20)

    def process_image(self, frame):
        """
        Process a webcam frame to isolate the hand using greyscale, thresholding, and contours.

        Args:
            frame (numpy.ndarray): Input frame from the webcam in BGR format.

        Returns:
            tuple: (grey, thresh, bg_removed)
                - grey: Grayscale image.
                - thresh: Thresholded binary image.
                - bg_removed: Frame with background removed using contours.
        """
        # Convert the frame to greyscale
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding to create a high-contrast image
        _, thresh = cv2.threshold(grey, 100, 255, cv2.THRESH_BINARY)

        # Find external contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create a single-channel mask for background removal
        mask = np.zeros(grey.shape, dtype=np.uint8)

        # Draw contours on the mask to isolate significant regions (e.g., hand)
        for contour in contours:
            if cv2.contourArea(contour) > 2000:  # Filter small contours based on area
                cv2.drawContours(mask, [contour], -1, 255, -1)  # Fill contour area with white

        # Apply the mask to remove the background
        bg_removed = cv2.bitwise_and(frame, frame, mask=mask)

        return grey, thresh, bg_removed

    def update_image(self, label, img):
        """
        Update a Tkinter label with a processed image.

        Args:
            label (tk.Label): The Tkinter label to update.
            img (numpy.ndarray): The image to display (BGR or grayscale).
        """
        img = cv2.resize(img, (200, 150))  # Resize for consistent display
        if len(img.shape) == 2:  # Handle grayscale images
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for Tkinter
        img_pil = Image.fromarray(img)  # Convert to PIL Image
        photo = ImageTk.PhotoImage(img_pil)  # Convert to Tkinter-compatible format
        label.config(image=photo)
        label.image = photo  # Keep reference to avoid garbage collection

    def update_frame(self):
        """
        Update the GUI with the latest webcam frame and processed images.
        Schedules itself to run periodically using Tkinter's after method.
        """
        ret, frame = self.cap.read()  # Capture frame from webcam
        if ret:
            frame = cv2.flip(frame, 1)  # Mirror the frame for natural viewing
            grey, thresh, bg_removed = self.process_image(frame)  # Process the frame
            # Update each panel with corresponding image
            self.update_image(self.webcam_label, frame)
            self.update_image(self.grey_label, grey)
            self.update_image(self.thresh_label, thresh)
            self.update_image(self.bg_label, bg_removed)
        self.root.after(10, self.update_frame)  # Schedule next update after 10ms

# Test function to demonstrate the GUI
if __name__ == "__main__":
    root = tk.Tk()  # Create the root Tkinter window
    app = GUIDemo(root)  # Initialize the GUI
    app.cap = cv2.VideoCapture(0)  # Open the default webcam
    if not app.cap.isOpened():
        print("Error: Could not open webcam.")
    else:
        print("Starting GUI demo. Place hand in front of webcam to see processed images. Close window to exit.")
        app.update_frame()  # Start updating frames
        root.mainloop()  # Run the Tkinter event loop
        app.cap.release()  # Release the webcam when done