# game/game.py

import json
import os
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from PIL import Image, ImageTk

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

                # Run drawing tasks in parallel
                with ThreadPoolExecutor() as executor:
                    futures = {
                        executor.submit(
                            player.provide_input, assigned_texts.get(player.name), phase='draw', round=self.round
                        ): player.name for player in self.players
                    }
                    for future in as_completed(futures):
                        player_name = futures[future]
                        try:
                            input_drawing = future.result()
                        except Exception as exc:
                            print(f"{player_name} generated an exception: {exc}")
                            input_drawing = "No drawing generated due to error."
                        round_data["drawings"][player_name] = input_drawing

            elif text_phase == 'guess_text':
                # Assign texts to players based on their guesses without self-assignment
                # Here, the texts to draw are the guesses themselves
                assigned_texts = self.distribute_texts(round_data["texts"])
                round_data["draw_assignments"] = assigned_texts  # Record text assignments

                # Run drawing tasks in parallel
                with ThreadPoolExecutor() as executor:
                    futures = {
                        executor.submit(
                            player.provide_input, assigned_texts.get(player.name), phase='draw', round=self.round
                        ): player.name for player in self.players
                    }
                    for future in as_completed(futures):
                        player_name = futures[future]
                        try:
                            input_drawing = future.result()
                        except Exception as exc:
                            print(f"{player_name} generated an exception: {exc}")
                            input_drawing = "No drawing generated due to error."
                        round_data["drawings"][player_name] = input_drawing

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
        Display the game history as separate chats for each chain using Tkinter.
        """
        # Create the main Tkinter window
        root = tk.Tk()
        root.title("Game History")

        # Use a notebook to organize chains in tabs
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill='both')

        # Get the initial texts from Round 1
        initial_texts = self.history[0]['texts']  # Round 1 texts

        # For each initial text, reconstruct the chain
        for starter_player, initial_text in initial_texts.items():
            # Create a frame for each chain
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=f"{starter_player}'s Chain")

            # Create a scrolled text widget for the chat
            chat_display = ScrolledText(frame, wrap='word', state='disabled')
            chat_display.pack(expand=True, fill='both')

            chain = []
            chain.append({
                'player': starter_player,
                'action': 'Text',
                'content': initial_text
            })

            current_content = initial_text

            # Iterate over the rounds, starting from Round 1
            for round_number in range(0, len(self.history)):
                round_data = self.history[round_number]

                # Identify who was assigned to draw the current content
                draw_assignments = round_data.get('draw_assignments', {})
                drawings = round_data.get('drawings', {})

                # Find the player assigned to draw the current content
                drawing_player = None
                for player_name, text in draw_assignments.items():
                    if text == current_content:
                        drawing_player = player_name
                        break

                if drawing_player:
                    # Add the drawing to the chain
                    drawing = drawings.get(drawing_player, 'No drawing')
                    chain.append({
                        'player': drawing_player,
                        'action': 'Drawing',
                        'content': drawing
                    })
                else:
                    break  # No drawing found; end of chain

                # For rounds beyond Round 1, find the guess for this drawing
                if round_number + 1 < len(self.history):
                    next_round_data = self.history[round_number + 1]
                    guess_assignments = next_round_data.get('guess_assignments', {})
                    texts = next_round_data.get('texts', {})

                    # Find the player who was assigned this drawing to guess
                    guessing_player = None
                    for player_name, drawing_assigned in guess_assignments.items():
                        if drawing_assigned == drawing:
                            guessing_player = player_name
                            break

                    if guessing_player:
                        # Add the guess to the chain
                        guess_text = texts.get(guessing_player, 'No guess')
                        chain.append({
                            'player': guessing_player,
                            'action': 'Guess',
                            'content': guess_text
                        })
                        # Update current content for the next round
                        current_content = guess_text
                    else:
                        break  # No guess found; end of chain
                else:
                    break  # Last round reached; end of chain

            # Inside the loop over entries in the chain
            for entry in chain:
                player = entry['player']
                action = entry['action']
                content = entry['content']

                # Enable the text widget to insert content
                chat_display.configure(state='normal')

                if action == 'Drawing' and os.path.exists(content):
                    # Display the image
                    try:
                        img = Image.open(content)
                        img.thumbnail((400, 400))  # Resize image if necessary
                        photo = ImageTk.PhotoImage(img)
                        chat_display.insert(tk.END, f"\n{player} ({action}):\n")
                        chat_display.image_create(tk.END, image=photo)
                        chat_display.insert(tk.END, "\n\n")
                        # Keep a reference to the image to prevent garbage collection
                        if not hasattr(chat_display, 'images'):
                            chat_display.images = []
                        chat_display.images.append(photo)
                    except Exception as e:
                        chat_display.insert(tk.END, f"{player} ({action}): [Error displaying image]\n\n")
                else:
                    # Format the message
                    message = f"{player} ({action}): {content}\n\n"
                    chat_display.insert(tk.END, message)

                # Disable the text widget to prevent user editing
                chat_display.configure(state='disabled')

        # Start the Tkinter main loop
        root.mainloop()
