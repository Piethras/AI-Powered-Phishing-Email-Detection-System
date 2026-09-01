// Placeholder - real Confidence Score Dashboard built on Day 18.
// This file exists now only to confirm the frontend project boots
// and can reach the Flask API's /api/health endpoint.
import { useState, useEffect } from "react";

function App() {
  const [status, setStatus] = useState("checking...");

  useEffect(() => {
    fetch("http://localhost:5000/api/health")
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("backend unreachable"));
  }, []);

  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>Phishing Detection Dashboard</h1>
      <p>Backend status: {status}</p>
      <p><em>Full dashboard UI arrives on Day 18.</em></p>
    </div>
  );
}

export default App;
