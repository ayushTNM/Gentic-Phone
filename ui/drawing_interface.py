import os
import tkinter as tk
from pathlib import Path
from sys import base_prefix

from PIL import Image, ImageDraw, ImageTk

os.environ["TCL_LIBRARY"] = str(Path(base_prefix) / "lib" / "tcl8.6")
os.environ["TK_LIBRARY"] = str(Path(base_prefix) / "lib" / "tk8.6")


def save_drawing(player_name, round):
    # Create a simple drawing canvas
    root = tk.Tk()
    root.title(f"{player_name} - Draw")

    canvas_width = 400
    canvas_height = 400
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack()

    drawing = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(drawing)
    last_x, last_y = None, None
    file_path = f"assets/drawings/{player_name}_drawing_{round}.png"

    def draw_line(event):
        nonlocal last_x, last_y
        if last_x and last_y:
            canvas.create_line(last_x, last_y, event.x, event.y, fill='black')
            draw.line([last_x, last_y, event.x, event.y], fill='black')
        last_x, last_y = event.x, event.y

    def reset(event):
        nonlocal last_x, last_y
        last_x, last_y = None, None

    def save_and_exit():
        os.makedirs("/".join(file_path.split("/")[:-1]), exist_ok=True)
        if os.path.exists(file_path):
            os.remove(file_path)
        drawing.save(file_path)
        root.destroy()

    canvas.bind("<B1-Motion>", draw_line)
    canvas.bind("<ButtonRelease-1>", reset)

    save_button = tk.Button(root, text="Save Drawing", command=save_and_exit)
    save_button.pack()

    root.mainloop()
    return file_path

def display_drawing(file_path):
    if not os.path.exists(file_path):
        print(f"Drawing file not found: {file_path}")
        return

    root = tk.Tk()
    root.title("Drawing to Guess")

    # Open the image using PIL
    image = Image.open(file_path)
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    label = tk.Label(root, image=photo)
    label.image = photo  # Keep a reference
    label.pack()

    # Add a close button
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack()

    root.mainloop()