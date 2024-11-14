# game/ai_player.py
import os
import random

from ai.ai_logic import generate_ai_drawing, generate_ai_guess, generate_ai_text
from game.player import Player
from ui.console_ui import display_message


class AIPlayer(Player):
    def provide_input(self, previous_output, phase, round):
        if phase == 'create_text':
            ai_text = generate_ai_text()
            display_message(f"{self.name} (AI) provides text: {ai_text}")
            return ai_text
        elif phase == 'guess_text':
            if previous_output:
                ai_guess = generate_ai_guess(previous_output)
                display_message(f"{self.name} (AI) guesses text: {ai_guess}")
                return ai_guess
            else:
                ai_guess = "No guess"
                display_message(f"{self.name} (AI) has no drawing to guess.")
                return ai_guess
        elif phase == 'draw':
            if isinstance(previous_output, str):
                # Assuming previous_output is a text prompt or a guess
                ai_drawing = generate_ai_drawing(previous_output)
                drawing_path = f"assets/drawings/{self.name}_drawing_{round}.png"
                # Here, generate_ai_drawing should return image bytes
                try:
                    # Ensure the drawings directory exists
                    drawings_dir = os.path.join("assets", "drawings")
                    os.makedirs(drawings_dir, exist_ok=True)

                    with open(drawing_path, 'wb') as f:
                        f.write(ai_drawing)
                    display_message(f"{self.name} (AI) provides a drawing: {drawing_path}")
                except Exception as e:
                    display_message(f"{self.name} (AI) failed to save drawing: {e}")
                    drawing_path = "No drawing"
                return drawing_path
            else:
                display_message(f"{self.name} (AI) has no prompt to draw.")
                return "No drawing"

    def receive_output(self, output, phase):
        # AI can process the received output if needed
        pass
