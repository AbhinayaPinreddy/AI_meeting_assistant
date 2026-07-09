from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from services.rag import ask_question
from pydantic import BaseModel

from database import engine
from database import Base
from database import SessionLocal

from models import Meeting
from models import Transcript
from models import Summary

from services.summarizer import generate_summary
from services.pdf_generator import create_pdf
from services.duration import get_audio_duration
from speaker_api import get_meeting_data



import os
class ChatRequest(BaseModel):
    question: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "AI Meeting Assistant Backend Running"
    }


@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):

    # Create uploads folder if not present
    os.makedirs("uploads", exist_ok=True)

    filepath = os.path.join("uploads", file.filename)

    # Save uploaded file
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())
    
    meeting_data = get_meeting_data(filepath)
    speaker_transcript = meeting_data["speaker_transcript"]
    transcript_text = meeting_data["transcript"]
    duration = get_audio_duration(filepath)

    print("Duration:", duration)

    db = SessionLocal()

    try:
        # Save meeting information
        meeting = Meeting(
            title=file.filename,
            filename=file.filename,
            filepath=filepath,
            duration=duration
        )

        db.add(meeting)
        db.commit()
        db.refresh(meeting)

        print("Meeting saved successfully!")

        # Generate transcript using Whisper

        print("Transcription completed!")

        # Save transcript
        # Save transcript
        transcript = Transcript(
            meeting_id=meeting.id,
            transcript_text=transcript_text,
            speaker_transcript=speaker_transcript
        )

        db.add(transcript)
        db.commit()

        print("Transcript saved successfully!")


        # Generate summary using Groq
        summary_text = generate_summary(transcript_text)

        print("Summary generated successfully!")

        # Save summary
        summary = Summary(
            meeting_id=meeting.id,
            summary_text=summary_text,
            action_items=""
        )

        db.add(summary)
        db.commit()

        print("Summary saved successfully!")

        return {
            "message": "Uploaded Successfully",
            "meeting_id": meeting.id,
            "filename": file.filename,
            "transcript": transcript_text,
            "speaker_transcript": speaker_transcript,
            "summary": summary_text
        }

    except Exception as e:
        db.rollback()
        return {
            "error": str(e)
        }

    finally:
        db.close()


@app.get("/meetings")
def get_meetings():

    db = SessionLocal()

    meetings = db.query(Meeting).all()

    result = []

    for meeting in meetings:
        result.append({
            "id": meeting.id,
            "title": meeting.title,
            "filename": meeting.filename,
            "filepath": meeting.filepath
        })

    db.close()

    return result


@app.get("/transcripts")
def get_transcripts():

    db = SessionLocal()

    transcripts = db.query(Transcript).all()

    result = []

    for transcript in transcripts:
        result.append({
            "id": transcript.id,
            "meeting_id": transcript.meeting_id,
            "transcript": transcript.transcript_text
        })

    db.close()

    return result


@app.get("/summaries")
def get_summaries():

    db = SessionLocal()

    summaries = db.query(Summary).all()

    result = []

    for summary in summaries:
        result.append({
            "id": summary.id,
            "meeting_id": summary.meeting_id,
            "summary": summary.summary_text,
            "action_items": summary.action_items
        })

    db.close()

    return result

@app.get("/meeting-history")
def meeting_history():

    db = SessionLocal()

    meetings = db.query(Meeting).all()

    result = []

    for meeting in meetings:

        summary = db.query(Summary).filter(
            Summary.meeting_id == meeting.id
        ).first()

        result.append({
            "id": meeting.id,
            "title": meeting.title,
            "filename": meeting.filename,
            "summary": summary.summary_text if summary else "",
            "created_at": meeting.created_at.strftime("%d %b %Y %I:%M %p"),
            "duration": meeting.duration
        })

    db.close()

    return result

@app.get("/meeting/{meeting_id}")
def get_meeting(meeting_id: int):

    db = SessionLocal()

    meeting = db.query(Meeting).filter(
        Meeting.id == meeting_id
    ).first()

    transcript = db.query(Transcript).filter(
        Transcript.meeting_id == meeting_id
    ).first()

    summary = db.query(Summary).filter(
        Summary.meeting_id == meeting_id
    ).first()

    db.close()

    return {
        "id": meeting.id,
        "title": meeting.title,
        "transcript": transcript.transcript_text if transcript else "",
        "summary": summary.summary_text if summary else "",
        "speaker_transcript": transcript.speaker_transcript if transcript else []
    }
@app.get("/download/{meeting_id}")
def download_pdf(meeting_id: int):

    db = SessionLocal()

    meeting = db.query(Meeting).filter(
        Meeting.id == meeting_id
    ).first()

    transcript = db.query(Transcript).filter(
        Transcript.meeting_id == meeting_id
    ).first()

    summary = db.query(Summary).filter(
        Summary.meeting_id == meeting_id
    ).first()

    if meeting is None:
        db.close()
        return {"error": "Meeting not found"}

    transcript_text = (
        transcript.transcript_text
        if transcript
        else "Transcript not available."
    )

    summary_text = (
        summary.summary_text
        if summary
        else "Summary not available."
    )

    os.makedirs("pdfs", exist_ok=True)

    pdf_path = f"pdfs/{meeting.filename}.pdf"

    create_pdf(
        meeting.filename,
        transcript_text,
        summary_text,
        pdf_path
    )

    db.close()

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{os.path.splitext(meeting.filename)[0]}.pdf"
    )

@app.post("/chat")
def chat(request: ChatRequest):

    answer = ask_question(request.question)

    return {
        "answer": answer
    }

@app.delete("/meeting/{meeting_id}")
def delete_meeting(meeting_id: int):

    db = SessionLocal()

    meeting = db.query(Meeting).filter(
        Meeting.id == meeting_id
    ).first()

    if meeting is None:
        db.close()
        return {"error": "Meeting not found"}

    # Delete transcript
    db.query(Transcript).filter(
        Transcript.meeting_id == meeting_id
    ).delete()

    # Delete summary
    db.query(Summary).filter(
        Summary.meeting_id == meeting_id
    ).delete()

    # Delete meeting
    db.delete(meeting)

    db.commit()

    db.close()

    return {
        "message": "Meeting deleted successfully"
    }