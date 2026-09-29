import React, { useState, useEffect } from "react";
import { API_BASE } from "../constants";

const VERDICT_LABELS = {
  true_positive: { text: "Confirmed Phishing", className: "badge--phishing" },
  false_positive: { text: "False Positive", className: "badge--risk-medium" },
  true_negative: { text: "Confirmed Legitimate", className: "badge--legit" },
  false_negative: { text: "Missed Phishing", className: "badge--risk-high" },
  // Legacy values from before the Day 19 verdict-labeling fix
  confirmed_phishing: { text: "Confirmed Phishing", className: "badge--phishing" },
};

export default function FeedbackReviewPage() {
  const [entries, setEntries] = useState([]);
  const [status, setStatus] = useState("loading");

  useEffect(() => {
    fetch(`${API_BASE}/feedback/all`)
      .then((r) => r.json())
      .then((data) => { setEntries(data); setStatus("ready"); })
      .catch(() => setStatus("error"));
  }, []);

  const counts = entries.reduce((acc, e) => {
    acc[e.user_verdict] = (acc[e.user_verdict] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="panel">
      <h2 className="panel__title">Feedback Review</h2>
      <p className="status-message" style={{ marginBottom: 16 }}>
        User-submitted feedback on scan results, for human review. This does not
        automatically alter classifier behavior or the whitelist &mdash; changes
        based on this feedback require a deliberate, separate action.
      </p>

      {status === "loading" && <p className="status-message">Loading...</p>}
      {status === "error" && <p className="status-message status-message--error">Could not load feedback.</p>}

      {status === "ready" && (
        <>
          <div className="stat-grid" style={{ marginBottom: 20 }}>
            {Object.entries(VERDICT_LABELS).map(([key, { text }]) => (
              <div key={key} className="settings-row" style={{ flexDirection: "column", alignItems: "flex-start", gap: 4 }}>
                <span className="stat-card__label">{text}</span>
                <span className="stat-card__value">{counts[key] || 0}</span>
              </div>
            ))}
          </div>

          {entries.length === 0 ? (
            <p className="status-message">No feedback submitted yet.</p>
          ) : (
            <table className="scans-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Sender</th>
                  <th>Subject</th>
                  <th>Verdict</th>
                </tr>
              </thead>
              <tbody>
                {entries.map((f) => {
                  const verdict = VERDICT_LABELS[f.user_verdict] || { text: f.user_verdict, className: "badge" };
                  const date = new Date(f.submitted_at);
                  return (
                    <tr key={f.feedback_id}>
                      <td className="muted" data-label="Date">
                        {date.toLocaleDateString(undefined, { month: "short", day: "numeric" })}, {date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                      </td>
                      <td className="truncate" data-label="Sender">{f.sender || "(unknown)"}</td>
                      <td className="truncate" data-label="Subject">{f.subject || "(no subject)"}</td>
                      <td data-label="Verdict"><span className={`badge ${verdict.className}`}>{verdict.text}</span></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </>
      )}
    </div>
  );
}