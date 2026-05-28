from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Key
api_key = os.getenv("GROQ_API_KEY")

# Groq client
client = Groq(api_key=api_key)

def summarize_text(text):

    prompt = f"""
    Summarize the following text into clear bullet points.

    Text:
    {text}
    """

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.5,
        max_tokens=1024
    )

    summary = response.choices[0].message.content

    return summary