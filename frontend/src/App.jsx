import { useState } from "react";

import UploadMeeting from "./components/UploadMeeting";
import TranscriptCard from "./components/TranscriptCard";
import SummaryCard from "./components/SummaryCard";
import MeetingHistory from "./components/MeetingHistory";
import ChatBox from "./components/ChatBox";
import SpeakerTranscriptCard from "./components/SpeakerTranscriptCard";

import "./App.css";

function App() {
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState("");
  const [speakerTranscript, setSpeakerTranscript] = useState([]);

  return (
    <div className="container">
      <h1>Welcome to MeetingHub</h1>

      <p className="subtitle">
        Turn every meeting into searchable insights with AI.
      </p>

      <UploadMeeting
        setTranscript={setTranscript}
        setSummary={setSummary}
        setSpeakerTranscript={setSpeakerTranscript}
      />
      <MeetingHistory
        setTranscript={setTranscript}
        setSummary={setSummary}
        setSpeakerTranscript={setSpeakerTranscript}
      />

      {transcript && (
        <TranscriptCard transcript={transcript} />
      )}

      {speakerTranscript.length > 0 && (
        <SpeakerTranscriptCard speakerTranscript={speakerTranscript}
    />
      )}

      {summary && (
        <SummaryCard summary={summary} />
      )}
      
      <ChatBox />
    </div>
  );
}

export default App;