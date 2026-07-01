import { useState } from "react";
import axios from "axios";

function ChatBox() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          question: question,
        }
      );

      setAnswer(response.data.answer);
    } catch (error) {
      alert("Failed to get response.");
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div className="card">
      <h2>💬 Chat With Meetings</h2>

      <textarea
        rows="3"
        placeholder="Ask anything about your meetings..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{
          width: "100%",
          padding: "12px",
          borderRadius: "8px",
          marginBottom: "15px",
          resize: "none",
        }}
      />

      <button onClick={askQuestion}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <div
          style={{
            marginTop: "20px",
            padding: "15px",
            background: "#273549",
            borderRadius: "10px",
            whiteSpace: "pre-wrap",
          }}
        >
          <h3>Answer</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default ChatBox;