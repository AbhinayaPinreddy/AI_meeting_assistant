from groq import Groq

from config import GROQ_API_KEY
from database import SessionLocal
from models import Meeting, Transcript

client = Groq(api_key=GROQ_API_KEY)


def ask_question(question):

    db = SessionLocal()

    meetings = db.query(Meeting).all()

    # -----------------------------
    # Direct database questions
    # -----------------------------
    q = question.lower()

    if "how many meeting" in q:

        db.close()

        return f"There are {len(meetings)} meetings stored in the database."

    if "list" in q and "meeting" in q:

        names = [m.filename for m in meetings]

        db.close()

        return "Meetings:\n\n" + "\n".join(names)

    # -----------------------------
    # Build context
    # -----------------------------

    context = ""

    for meeting in meetings:

        transcript = db.query(Transcript).filter(
            Transcript.meeting_id == meeting.id
        ).first()

        if transcript:
            speaker_text = ""

            if transcript.speaker_transcript:

                for item in transcript.speaker_transcript:

                    speaker_text += (
                        f"{item['speaker']}: {item['text']}\n"
                    )

            context += f"""
Meeting ID: {meeting.id}

Meeting Name:
{meeting.filename}

Transcript:
{transcript.transcript_text}

Speaker Transcript:
{speaker_text}

=================================
"""

    db.close()

    prompt = f"""
You are an AI Meeting Assistant.

The following are MULTIPLE meeting transcripts.

Each transcript belongs to a different meeting.

If the user asks about ALL meetings,
consider every transcript.

If the user asks about ONE meeting,
identify the correct meeting.

If information is unavailable,
say you don't know.

Meeting Transcripts:

{context}

User Question:

{question}

Answer:
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