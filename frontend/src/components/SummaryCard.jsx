function SummaryCard({ summary }) {
  return (
    <div className="card">
      <h2>Summary</h2>
      <pre>{summary}</pre>
    </div>
  );
}

export default SummaryCard;