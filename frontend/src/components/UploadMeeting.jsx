import { useState } from "react";
import axios from "axios";

function UploadMeeting({ setTranscript, setSummary, setSpeakerTranscript }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadFile = async () => {
    if (!file) {
      alert("Select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await axios.post(
        "https://ai-meeting-assistant-backend-3gqm.onrender.com/upload",
        formData
      );
      console.log("UPLOAD RESPONSE:", response.data);
      setTranscript(response.data.transcript || "");
      setSummary(response.data.summary || "");
      setSpeakerTranscript(response.data.speaker_transcript || []);

      setLoading(false);
    } catch (error) {
      console.error(error);
      alert("Upload failed");
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Upload Meeting</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br />
      <br />

      <button onClick={uploadFile}>
        Upload
      </button>

      {loading && <p>Processing Meeting...</p>}
    </div>
  );
}

export default UploadMeeting;