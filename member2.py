"""
Image Processing Module for Rock Paper Scissors Game
Author: Kavidu Nimantha
Date: May 08, 2025
Description: This module implements an image processing pipeline to convert webcam frames
into greyscale, thresholded, and background-removed images. It detects contours to isolate
the hand and supports visualization for debugging.
"""

import cv2  # OpenCV for image processing and webcam capture
import numpy as np  # NumPy for numerical operations and array handling

def process_image(frame):
    """
    Process a webcam frame to isolate the hand using greyscale, thresholding, and contours.

    Args:
        frame (numpy.ndarray): Input frame from the webcam in BGR format.

    Returns:
        tuple: (grey, thresh, bg_removed, contours)
            - grey: Grayscale image.
            - thresh: Thresholded binary image.
            - bg_removed: Frame with background removed using contours.
            - contours: List of detected contours.
    """
    # Convert the frame to greyscale for processing
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding to create a high-contrast image
    _, thresh = cv2.threshold(grey, 100, 255, cv2.THRESH_BINARY)

    # Find external contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a single-channel mask for background removal
    mask = np.zeros(grey.shape, dtype=np.uint8)  # Single-channel mask matching greyscale dimensions

    # Draw contours on the mask to isolate significant regions (e.g., hand)
    for contour in contours:
        if cv2.contourArea(contour) > 2000:  # Filter small contours based on area
            cv2.drawContours(mask, [contour], -1, 255, -1)  # Fill contour area with white

    # Apply the mask to remove the background, keeping only the hand region
    bg_removed = cv2.bitwise_and(frame, frame, mask=mask)

    return grey, thresh, bg_removed, contours

# Test function to demonstrate image processing pipeline
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # Open the default webcam
    if not cap.isOpened():
        print("Error: Could not open webcam.")
    else:
        print("Starting image processing demo. Place hand in front of webcam. Press 'q' to quit.")
        while True:
            ret, frame = cap.read()  # Capture frame from webcam
            if not ret:
                print("Error: Could not read frame.")
                break
            frame = cv2.flip(frame, 1)  # Mirror the frame for natural viewing
            grey, thresh, bg_removed, contours = process_image(frame)  # Process the frame
            print(f"Contours found: {len(contours)}")  # Output number of detected contours
            # Convert greyscale and thresholded images to RGB for display
            grey_rgb = cv2.cvtColor(grey, cv2.COLOR_GRAY2RGB)
            thresh_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
            # Display all stages of processing
            cv2.imshow("Original", frame)
            cv2.imshow("Greyscale", grey_rgb)
            cv2.imshow("Thresholded", thresh_rgb)
            cv2.imshow("Background Removed", bg_removed)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key
                break
        cap.release()  # Release the webcam
        cv2.destroyAllWindows()  # Close all OpenCV windows