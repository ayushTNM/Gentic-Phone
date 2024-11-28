# ai/ai_logic.py
import io
import random

import google.generativeai as genai
import requests
from PIL import Image


def generate_ai_text(model):
    """
    Generates a unique text prompt using Google's Gemini model.
    """
    try:
        prompt = "We're playing Gartic Phone. Come up with something to draw. Give a short answer, starting with A/An. Use your creativity."
        # Initialize the Gemini model (assuming 'text-generation' is the correct model name)
        response = model.generate_content([prompt], generation_config={"temperature":1.5})
        ai_text = response.text.strip()
        print(f"DEBUG: Gemini generated text: {ai_text}")  # Debug statement
        return ai_text
    except Exception as e:
        print(f"Error generating AI text: {e}")
        # Fallback to predefined responses in case of an error
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
    """
    Generates a guess based on a drawing using Google's Gemini model.
    
    Parameters:
        drawing_path (str): The file path to the drawing image.
        model: The Gemini model instance.
    
    Returns:
        str: The AI's guess text.
    """
    try:
        # Upload the image file to Gemini (assuming 'upload_file' is the correct method)
        image = genai.upload_file(drawing_path)
        prompt = "We're playing Gartic Phone. What do you think this drawing is trying to show? Give a short answer, starting with A/An. Use your creativity."
        response = model.generate_content([image, "\n", prompt])
        ai_guess = response.text.strip()
        print(f"DEBUG: Gemini generated guess: {ai_guess}")  # Debug statement
        return ai_guess
    except Exception as e:
        print(f"Error generating AI guess: {e}")
        # Fallback: Return a generic guess
        return "No guess"


def generate_ai_drawing(prompt, model):
    """
    Generates an image based on the provided prompt using Google's Gemini model.
    Returns the image bytes.
    """
    try:
        # Encode the prompt for URL inclusion
        
        return requests.get(
            url=model.generate(
                prompt = f"Colorless doodle of {prompt}",
                negative = "Color, realism",
                save = False,
            ).params["url"],
            headers={"Content-Type": "application/json"},
            timeout=30,
        ).content
    except Exception as e:
        print(f"Error generating ai image: {e}")
        return load_image(Image.open("temp_ai_img.jpg"))


def load_image(img):
    """
    Loads an image.
    """
    byte_io = io.BytesIO()
    img.save(byte_io, format='PNG')
    
    # Retrieve the byte data
    byte_data = byte_io.getvalue()
    return byte_data

