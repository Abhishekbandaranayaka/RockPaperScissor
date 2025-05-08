"""
Game Logic Module for Rock Paper Scissors Game
Author: Gayathri Konara 
Index Number : 22976
Date: May 08, 2025
Description: This module implements the game logic to determine winners in Rock Paper Scissors
(RPS) and Rock Paper Scissors Lizard Spock (RPSLS) modes. It includes a test suite to verify
all game scenarios (Win, Lose, Tie, invalid gestures).
"""

import random  # Random module for generating AI choices in tests

class GameLogic:
    def __init__(self):
        """
        Initialize the GameLogic with available choices for each game mode.
        """
        self.choices = {
            "RPS": ["Rock", "Paper", "Scissors"],  # Choices for RPS mode
            "RPSLS": ["Rock", "Paper", "Scissors", "Lizard", "Spock"]  # Choices for RPSLS mode
        }

    def determine_winner(self, player_choice, ai_choice, game_mode="RPS"):
        """
        Determine the winner of a game round based on player and AI choices.

        Args:
            player_choice (str): The gesture chosen by the player.
            ai_choice (str): The gesture chosen by the AI.
            game_mode (str): The game mode, either "RPS" or "RPSLS" (default: "RPS").

        Returns:
            str: Result of the game ("Win", "Lose", "Tie", or "Invalid gesture").
        """
        # Check for invalid gestures
        if player_choice not in self.choices[game_mode] or ai_choice not in self.choices[game_mode]:
            return "Invalid gesture"
        # Check for tie
        if player_choice == ai_choice:
            return "Tie"
        # Define victory conditions based on game mode
        victories = {
            "Rock": ["Scissors", "Lizard"],
            "Paper": ["Rock", "Spock"],
            "Scissors": ["Paper", "Lizard"],
            "Lizard": ["Spock", "Paper"],
            "Spock": ["Scissors", "Rock"]
        } if game_mode == "RPSLS" else {
            "Rock": ["Scissors"],
            "Paper": ["Rock"],
            "Scissors": ["Paper"]
        }
        # Determine winner based on victory conditions
        return "Win" if ai_choice in victories[player_choice] else "Lose"

# Test function to demonstrate and validate game logic
if __name__ == "__main__":
    game = GameLogic()  # Create an instance of GameLogic
    game_modes = ["RPS", "RPSLS"]  # List of game modes to test
    test_cases = {
        "RPS": [("Rock", "Scissors"), ("Paper", "Rock"), ("Scissors", "Paper"), ("Rock", "Rock"), ("Invalid", "Rock")],
        "RPSLS": [("Rock", "Scissors"), ("Paper", "Spock"), ("Scissors", "Lizard"), ("Lizard", "Paper"), ("Spock", "Rock"),
                  ("Rock", "Rock"), ("Invalid", "Spock")]
    }  # Predefined test cases for each mode

    # Run tests for each game mode
    for mode in game_modes:
        print(f"\nTesting {mode} mode:")
        for player, ai in test_cases[mode]:
            result = game.determine_winner(player, ai, mode)  # Determine result for each test case
            print(f"Player: {player}, AI: {ai}, Result: {result}")  # Output test result
        # Perform additional random tests
        print("\nRandom Tests for", mode)
        for _ in range(5):  # Run 5 random tests
            player = random.choice(game.choices[mode])  # Random player choice
            ai = random.choice(game.choices[mode])  # Random AI choice
            result = game.determine_winner(player, ai, mode)  # Determine result
            print(f"Player: {player}, AI: {ai}, Result: {result}")  # Output random test result