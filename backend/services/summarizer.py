from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def generate_summary(transcript):

    prompt = f"""
    Analyze the meeting transcript and return exactly in this format:

    SUMMARY:
    <summary>

    KEY POINTS:
    - point 1
    - point 2

    ACTION ITEMS:
    - action 1
    - action 2

    Transcript:
    {transcript}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content