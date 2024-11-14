# game/game.py
import json
import os
import random

from ui.console_ui import display_message


class Game:
    def __init__(self, players):
        self.players = players  # List of Player instances
        self.round = 0
        self.history = []  # To track game history

    def start(self, rounds=5):
        for _ in range(rounds):
            self.round += 1
            display_message(f"\n--- Round {self.round} ---")

            # Determine the type of text phase
            if self.round == 1:
                text_phase = 'create_text'
                display_message("Phase 1: Text Creation")
            else:
                text_phase = 'guess_text'
                display_message("Phase 1: Text Guessing")

            # Phase 1: Text Phase (Creation or Guessing)
            round_data = {"round": self.round, "texts": {}, "drawings": {}}
            if self.round == 1:
                # No previous drawings to guess
                previous_drawings = None
            else:
                # Get drawings from the previous round
                previous_drawings = self.history[-1]['drawings']

            # Distribute prompts based on the phase
            if text_phase == 'create_text':
                # Round 1: Players create original texts
                for player in self.players:
                    input_text = player.provide_input(None, phase='create_text', round=self.round)
                    round_data["texts"][player.name] = input_text
            elif text_phase == 'guess_text':
                # Rounds 2+: Players guess texts based on previous drawings
                # Distribute previous drawings to players, ensuring no self-assignment
                assigned_drawings = self.distribute_drawings(previous_drawings)
                for player in self.players:
                    drawing_path = assigned_drawings.get(player.name)
                    input_guess = player.provide_input(drawing_path, phase='guess_text', round=self.round)
                    round_data["texts"][player.name] = input_guess

            # Phase 2: Drawing Phase
            display_message("Phase 2: Drawing")
            for player in self.players:
                target_text = self.get_next_text_for_player(player, round_data["texts"])
                if text_phase == 'create_text':
                    input_drawing = player.provide_input(target_text, phase='draw', round=self.round)
                elif text_phase == 'guess_text':
                    input_drawing = player.provide_input(target_text, phase='draw', round=self.round)

                round_data["drawings"][player.name] = input_drawing

            self.history.append(round_data)

        # Save history to a file
        self.save_history()
        display_message("\nGame history saved to 'game_history.json'")

    def distribute_drawings(self, previous_drawings):
        """
        Distribute previous round's drawings among players for guessing.
        Ensures each player gets exactly one drawing and no drawing is assigned to multiple players.
        Also ensures that players do not guess their own drawings.
        """
        if not previous_drawings:
            return {}

        # Create a list of (player_name, drawing_path) tuples
        drawings = list(previous_drawings.items())

        # Shuffle the list to randomize distribution
        random.shuffle(drawings)

        # Assign drawings to players, ensuring no self-assignment
        assigned_drawings = {}
        for player in self.players:
            for i, (drawer, drawing_path) in enumerate(drawings):
                if drawer != player.name and drawing_path not in assigned_drawings.values():
                    assigned_drawings[player.name] = drawing_path
                    # Remove the assigned drawing to prevent reuse
                    del drawings[i]
                    break
            else:
                # If no suitable drawing found (all remaining are player's own), assign None
                assigned_drawings[player.name] = None

        return assigned_drawings

    def get_next_text_for_player(self, current_player, current_texts):
        """
        Assign each player to draw based on the next player's text, ensuring no self-assignment.
        """
        idx = self.players.index(current_player)
        num_players = len(self.players)
        for offset in range(1, num_players):
            target_player = self.players[(idx + offset) % num_players]
            if target_player.name != current_player.name:
                return current_texts[target_player.name]
        # Fallback if no other player is found (which shouldn't happen)
        return "No prompt"

    def save_history(self):
        """
        Save the game history to a JSON file.
        """
        with open("game_history.json", "w") as f:
            json.dump(self.history, f, indent=4)

    def display_history(self):
        """
        Display the game history in the console.
        """
        display_message("\n--- Game History ---")
        for round_data in self.history:
            display_message(f"\nRound {round_data['round']}:")
            display_message("Texts:")
            for player, text in round_data["texts"].items():
                display_message(f"  {player}: {text}")
            display_message("Drawings:")
            for player, drawing in round_data["drawings"].items():
                display_message(f"  {player}: {drawing}")
