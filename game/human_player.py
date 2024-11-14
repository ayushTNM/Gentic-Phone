# game/human_player.py
import os

from game.player import Player
from ui.console_ui import display_message, get_user_input
from ui.drawing_interface import display_drawing, save_drawing


class HumanPlayer(Player):
    def provide_input(self, previous_output, phase, round):
        if phase == 'create_text':
            user_input = get_user_input(f"{self.name}, enter your text prompt: ")
            return user_input
        elif phase == 'guess_text':
            if previous_output and os.path.exists(previous_output):
                display_message(f"{self.name}, guess the text based on the drawing:")
                display_drawing(previous_output)
                user_input = get_user_input("Your guess: ")
                return user_input
            else:
                display_message(f"{self.name}, no drawing available to guess.")
                return "No guess"
        elif phase == 'draw':
            if isinstance(previous_output, str):
                # Assuming previous_output is a text prompt or a guess
                display_message(f"{self.name}, please draw based on the prompt: {previous_output}")
                drawing_path = save_drawing(self.name, round)
                return drawing_path
            else:
                display_message(f"{self.name}, please draw based on the prompt: {previous_output}")
                drawing_path = save_drawing(self.name, round)
                return drawing_path

    def receive_output(self, output, phase):
        if phase in ['create_text', 'guess_text']:
            display_message(f"{self.name} received text: {output}")
        elif phase == 'draw':
            display_message(f"{self.name} received drawing: {output}")
