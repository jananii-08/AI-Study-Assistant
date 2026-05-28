from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Key
api_key = os.getenv("GROQ_API_KEY")

# Groq client
client = Groq(api_key=api_key)

def generate_quiz(topic):

    prompt = f"""
    Generate 10 multiple choice quiz questions from the following topic.

    IMPORTANT RULES:

    1. Do NOT show answers with questions.
    2. At the end write:
       ANSWERS:
    3. In the answers section include:
       - Correct option letter
       - Full correct answer text

    Example:

    1. B) Python is an interpreted language

    Topic:
    {topic}
    """

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7,
        max_tokens=1500
    )

    full_text = response.choices[0].message.content

    # Split quiz and answers
    if "ANSWERS:" in full_text:

        quiz_part, answers_part = full_text.split("ANSWERS:", 1)

    else:

        quiz_part = full_text
        answers_part = "Answers not available."

    return quiz_part, answers_part