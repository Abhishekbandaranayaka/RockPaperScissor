"""
Speech Recognition Module for Rock Paper Scissors Game
Author: [Udeshi Wijesekara] (Member 4)
Index Number : 22826
Date: May 08, 2025
Description: This module implements speech recognition to detect the phrase
"Rock, Paper, Scissors, Shoot" as a trigger for starting a game round. It uses
the SpeechRecognition library with Google Speech Recognition API and includes
robust error handling and retry logic.
"""

import speech_recognition as sr  # SpeechRecognition library for speech-to-text

class SpeechHandler:
    def __init__(self):
        """
        Initialize the SpeechHandler with a recognizer and configuration settings.
        """
        self.recognizer = sr.Recognizer()  # Create a recognizer instance
        self.recognizer.energy_threshold = 4000  # Set energy threshold for speech detection sensitivity
        self.recognizer.pause_threshold = 1.0  # Set pause threshold for detecting end of speech
        self.attempts = 0  # Track number of recognition attempts
        self.max_attempts = 3  # Maximum number of attempts before giving up

    def listen_for_phrase(self):
        """
        Listen for the phrase "Rock, Paper, Scissors, Shoot" using the microphone.

        Returns:
            bool: True if the phrase is detected, False otherwise.
        """
        with sr.Microphone() as source:  # Open the microphone for input
            print("Adjusting for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)  # Calibrate for background noise
            while self.attempts < self.max_attempts:
                try:
                    self.attempts += 1  # Increment attempt counter
                    print(f"Listening for 'Rock, Paper, Scissors, Shoot'... (Attempt {self.attempts}/{self.max_attempts})")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Capture audio with timeout
                    text = self.recognizer.recognize_google(audio).lower()  # Convert audio to text using Google API
                    print(f"Recognized: {text}")  # Output recognized text
                    if "rock paper scissors shoot" in text:
                        print("Phrase detected!")
                        return True  # Phrase detected successfully
                    else:
                        print("Phrase not recognized.")
                        return False  # Phrase not matched
                except sr.UnknownValueError:
                    # Handle case where speech is unintelligible
                    print(f"Speak clearly and try again (Attempt {self.attempts}/{self.max_attempts})")
                    if self.attempts >= self.max_attempts:
                        print("Too many failed attempts. Resetting...")
                        self.attempts = 0
                    return False
                except sr.RequestError as e:
                    # Handle API request errors (e.g., no internet)
                    print(f"Speech recognition error: {e}")
                    return False
                except sr.WaitTimeoutError:
                    # Handle case where no speech is detected within timeout
                    print("No speech detected within timeout.")
                    return False
                except Exception as e:
                    # Handle unexpected errors
                    print(f"Unexpected error: {e}")
                    return False
        return False  # Return False if max attempts reached

# Test function to demonstrate speech recognition
if __name__ == "__main__":
    speech_handler = SpeechHandler()  # Create an instance of SpeechHandler
    print("Starting speech recognition demo. Say 'Rock, Paper, Scissors, Shoot' to trigger a round.")
    while True:
        if speech_handler.listen_for_phrase():  # Attempt to detect the trigger phrase
            print("Game round would start here!")
            speech_handler.attempts = 0  # Reset attempts after successful detection
            break
        else:
            if speech_handler.attempts >= speech_handler.max_attempts:
                print("Exiting after maximum attempts.")
                break  # Exit after reaching maximum failed attempts