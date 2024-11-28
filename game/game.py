# game/game.py

import json

from ui.console_ui import display_message
from utils.derangement import derangement


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
            round_data = {
                "round": self.round,
                "texts": {},
                "draw_assignments": {},  # Assignments of texts to players for drawing
                "guess_assignments": {},  # Assignments of drawings to players for guessing
                "drawings": {}
            }

            if self.round == 1:
                # No previous drawings to guess
                previous_drawings = None
            else:
                # Get drawings from the previous round
                previous_drawings = self.history[-1]['drawings']

            # Phase 1: Handle Text Creation or Guessing
            if text_phase == 'create_text':
                # Round 1: Players create original texts
                for player in self.players:
                    input_text = player.provide_input(None, phase='create_text', round=self.round)
                    round_data["texts"][player.name] = input_text
            elif text_phase == 'guess_text':
                # Rounds 2+: Players guess texts based on previous drawings
                # Distribute previous drawings among players without self-assignment
                assigned_drawings = self.distribute_drawings(previous_drawings)
                round_data["guess_assignments"] = assigned_drawings  # Record guess assignments
                for player in self.players:
                    drawing_path = assigned_drawings.get(player.name)
                    input_guess = player.provide_input(drawing_path, phase='guess_text', round=self.round)
                    round_data["texts"][player.name] = input_guess

            # Phase 2: Drawing Phase
            display_message("Phase 2: Drawing")

            if text_phase == 'create_text':
                # Assign texts to players for drawing without self-assignment
                assigned_texts = self.distribute_texts(round_data["texts"])
                round_data["draw_assignments"] = assigned_texts  # Record text assignments

                for player in self.players:
                    target_text = assigned_texts.get(player.name)
                    input_drawing = player.provide_input(target_text, phase='draw', round=self.round)
                    round_data["drawings"][player.name] = input_drawing

            elif text_phase == 'guess_text':
                # Assign texts to players based on their guesses without self-assignment
                # Here, the texts to draw are the guesses themselves
                assigned_texts = self.distribute_texts(round_data["texts"])
                round_data["draw_assignments"] = assigned_texts  # Record text assignments

                for player in self.players:
                    target_text = assigned_texts.get(player.name)
                    input_drawing = player.provide_input(target_text, phase='draw', round=self.round)
                    round_data["drawings"][player.name] = input_drawing

            self.history.append(round_data)
            print(self.history)

        # Save history to a file
        # self.save_history()
        display_message("\nGame history saved to 'game_history.json'")

    def distribute_drawings(self, previous_drawings):
        """
        Distribute previous round's drawings among players for guessing.
        Ensures each player gets exactly one drawing and no drawing is assigned to themselves.
        Utilizes derangement to prevent self-assignment.
        Returns a dictionary mapping player names to drawing paths.
        """
        if not previous_drawings:
            return {}

        players = self.players.copy()
        drawers = [player.name for player in self.players]
        drawings = [previous_drawings[drawer] for drawer in drawers]

        # Generate a derangement of the drawings
        deranged_drawings = derangement(drawings)

        if deranged_drawings is None:
            display_message("Error: Unable to generate derangement for drawings.")
            return {player.name: None for player in self.players}

        assigned_drawings = {player.name: drawing for player, drawing in zip(players, deranged_drawings)}
        for player_name, drawing in assigned_drawings.items():
            if drawing is None:
                display_message(f"Warning: {player_name} has no drawing assigned for guessing.")
            else:
                print(f"DEBUG: Assigned drawing '{drawing}' to {player_name} for guessing.")

        return assigned_drawings

    def distribute_texts(self, texts):
        """
        Distribute texts among players for drawing.
        Ensures each player draws exactly one text and no player draws their own text.
        Utilizes derangement to prevent self-assignment.
        Returns a dictionary mapping player names to texts they should draw.
        """
        if not texts:
            return {}

        players = self.players.copy()
        original_texts = [texts[player.name] for player in players]

        # Generate a derangement of the texts
        deranged_texts = derangement(original_texts)

        if deranged_texts is None:
            display_message("Error: Unable to generate derangement for texts.")
            return {player.name: "No prompt" for player in self.players}

        assigned_texts = {player.name: text for player, text in zip(players, deranged_texts)}
        for player_name, text in assigned_texts.items():
            if text == "No prompt":
                display_message(f"Warning: {player_name} has no text assigned for drawing.")
            else:
                print(f"DEBUG: Assigned text '{text}' to {player_name} for drawing.")

        return assigned_texts

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
            if "guess_assignments" in round_data:
                display_message("Guess Assignments:")
                for player, drawing in round_data["guess_assignments"].items():
                    display_message(f"  {player}: {drawing}")
            if "draw_assignments" in round_data:
                display_message("Draw Assignments:")
                for player, text in round_data["draw_assignments"].items():
                    display_message(f"  {player}: {text}")
            display_message("Drawings:")
            for player, drawing in round_data["drawings"].items():
                display_message(f"  {player}: {drawing}")
