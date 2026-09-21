import React, { useState } from "react";
import { API_BASE } from "../constants";

export default function ScanEmailPage({ onScanned }) {
  const [sender, setSender] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState(null);

  const handleScan = async () => {
    if (!body.trim()) { setError("Email body is required."); return; }
    setScanning(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sender, subject, body }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Scan failed");
      onScanned(data);
      setSender(""); setSubject(""); setBody("");
    } catch (err) {
      setError(err.message);
    } finally {
      setScanning(false);
    }
  };

  return (
    <div className="panel">
      <h2 className="panel__title">Scan an Email Manually</h2>
      <div className="scan-form">
        <input className="scan-form__input" placeholder="Sender (e.g. security@example.com)" value={sender} onChange={(e) => setSender(e.target.value)} />
        <input className="scan-form__input" placeholder="Subject" value={subject} onChange={(e) => setSubject(e.target.value)} />
        <textarea className="scan-form__textarea" placeholder="Paste the email body here..." rows={8} value={body} onChange={(e) => setBody(e.target.value)} />
        {error && <p className="upload-panel__error">{error}</p>}
        <button className="scan-form__submit" onClick={handleScan} disabled={scanning}>
          {scanning ? "Scanning..." : "Scan Email"}
        </button>
      </div>
    </div>
  );
}