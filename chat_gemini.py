# Import required libraries

import os  # For accessing environment variables
from dotenv import load_dotenv  # To load environment variables from a .env file
import google.generativeai as genai  # Google Generative AI SDK for interacting with Gemini models

# Load environment variables from the .env file
load_dotenv()

class ChatGemini:
    """
    ChatGemini is a helper class for interacting with Google's Gemini API.
    It loads the API key from the .env file, initializes the model,
    and provides a method to get responses from the model.
    """
    
    def __init__(self):
        """
        Initialize the Gemini API client.
        Loads the API key from environment variables and configures the SDK.
        """
        api_key = os.getenv("GEMINI_API_KEY")  # Fetch API key from .env file
        if not api_key:
            raise ValueError(" GEMINI_API_KEY not found in .env file.")  # Raise error if missing
        
        # Configure the Gemini SDK with the API key
        genai.configure(api_key=api_key)
        
        # Initialize the generative model (updated to the latest version)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def get_response(self, prompt):
        """
        Generates a text response from the Gemini model based on the given prompt.
        
        Parameters:
            prompt (str): The input text prompt to send to the Gemini model.
        
        Returns:
            str: The model's generated text response, or an error message if an exception occurs.
        """
        try:
            # Generate a response using the Gemini model
            response = self.model.generate_content(prompt)
            return response.text  # Extract and return the text from the response
        except Exception as e:
            # Catch and return any API or network-related errors
            return f" Gemini API Error: {e}"






