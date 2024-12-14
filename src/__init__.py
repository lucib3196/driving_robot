# main.py
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()

# Access the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("API key not found!")
else:
    print(f"Using API key: {openai.api_key}")

