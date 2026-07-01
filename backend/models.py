from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from sqlalchemy import JSON

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    filename = Column(String)

    filepath = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    duration = Column(String)


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    transcript_text = Column(Text)

    speaker_transcript = Column(JSON, nullable=True)


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    summary_text = Column(Text)
    action_items = Column(Text)