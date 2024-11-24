# ai/ai_logic.py
import io
import random

import google.generativeai as genai
from PIL import Image


def generate_ai_text():
    # Placeholder logic for AI text creation; replace with actual AI logic or more sophisticated generation
    responses = [
        "A sunny day at the beach.",
        "A cat chasing a mouse.",
        "An astronaut floating in space.",
        "A dragon flying over a castle.",
        "A robot making coffee.",
        "A magical forest with unicorns.",
        "A pirate ship battling a sea monster."
    ]
    return random.choice(responses)

def generate_ai_guess(drawing_path, model):
    image = genai.upload_file(drawing_path)
    prompt = "We're playing Gentic Phone. What do you think this drawing is trying to show? Give a short answer, starting with A/An. Use your creativity."
    response = model.generate_content([image, "\n", prompt])
    return response.text

def generate_ai_drawing(prompt):
    # Placeholder: Return empty bytes or integrate with an image generation API
    # For demonstration, we'll return empty bytes to represent an image
    # Replace this with actual image generation logic if desired
    img = Image.open("temp_ai_img.jpg")
    # Create a BytesIO object to save the image in memory
    byte_io = io.BytesIO()
    img.save(byte_io, format='PNG')
    
    # Retrieve the byte data
    byte_data = byte_io.getvalue()
    return byte_data