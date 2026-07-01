import { useEffect, useState } from "react";
import axios from "axios";

function MeetingHistory({
  setTranscript,
  setSummary,
  setSpeakerTranscript
}) {
  const [meetings, setMeetings] = useState([]);

  useEffect(() => {
    fetchMeetings();
  }, []);

  const fetchMeetings = async () => {
    const response = await axios.get(
      "http://127.0.0.1:8000/meeting-history"
    );

    setMeetings(response.data);
  };

  const loadMeeting = async (id) => {
    const response = await axios.get(
      `http://127.0.0.1:8000/meeting/${id}`
    );

    setTranscript(response.data.transcript);
    setSummary(response.data.summary);
    setSpeakerTranscript(response.data.speaker_transcript);
  };

  return (
    <div className="card">
      <h2>📁 Meeting History</h2>

      <h3 style={{ marginBottom: "20px" }}>
        Total Meetings: {meetings.length}
      </h3>

      {meetings.map((meeting) => (
        <div
          key={meeting.id}
          style={{
            background: "#273549",
            color: "white",
            border: "1px solid #4b5563",
            borderRadius: "12px",
            padding: "18px",
            marginBottom: "20px",
            boxShadow: "0px 4px 10px rgba(0,0,0,0.3)"
          }}
        >
          <h3
            style={{
              color: "#60a5fa",
              marginBottom: "10px"
            }}
          >
            📄 {meeting.filename}
          </h3>

          <p
            style={{
              color: "#d1d5db",
              marginBottom: "15px",
              fontSize: "14px",
              lineHeight: "1.8"
            }}
          >
            📅 Uploaded: {meeting.created_at}
            <p>⏱ Duration: {meeting.duration}</p>
          </p>

          <div
            style={{
              display: "flex",
              gap: "12px"
            }}
          >
            <button
              onClick={() => loadMeeting(meeting.id)}
            >
              👁 View Meeting
            </button>

            <button
              onClick={() =>
                window.open(
                  `http://127.0.0.1:8000/download/${meeting.id}`,
                  "_blank"
                )
              }
            >
              📄 Download PDF
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default MeetingHistory;