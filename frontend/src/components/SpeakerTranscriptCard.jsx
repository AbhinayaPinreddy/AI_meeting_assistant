function SpeakerTranscriptCard({ speakerTranscript }) {
    if(!speakerTranscript || speakerTranscript.length === 0) {
        return null;
    }
    return (
        <div className="card">
            <h2>Speaker Transcript</h2>

            {speakerTranscript.map((item, index) => (
                <div key={index} style={{ marginBottom: "15px" }}>
                    <strong>{item.speaker}</strong>

                    <p>{item.text}</p>

                    <hr />
                </div>
            ))}
        </div>
    );
}

export default SpeakerTranscriptCard;