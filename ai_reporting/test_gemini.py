import os
from dotenv import load_dotenv
from google import genai

# Load the key from .env into the environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("No API key found. Check your .env file has GEMINI_API_KEY set.")
    exit()

# Connect to Gemini and ask one simple test question
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="In one sentence, what is a data pipeline?"
)

print("Gemini says:")
print(response.text)