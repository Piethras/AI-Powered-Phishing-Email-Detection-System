import React, { useState } from "react";
import { Eye, ThumbsUp, ThumbsDown } from "lucide-react";
import { RiskBadge, StatusBadge } from "./Badges";
import { riskLevel } from "../utils";
import { API_BASE } from "../constants";
const FILTER_LABELS = { all: "All", phishing: "Phishing", legitimate: "Legitimate", uncertain: "Needs Review" };

export default function ScansTable({ predictions }) {
  const [filter, setFilter] = useState("all");
  const [expandedId, setExpandedId] = useState(null);
  const [feedbackGiven, setFeedbackGiven] = useState({});

  const filtered = predictions.filter((p) => filter === "all" || p.predicted_label === filter);

  const submitFeedback = async (emailId, verdict, rowKey, e) => {
    e.stopPropagation();
    try {
      const res = await fetch(`${API_BASE}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email_id: emailId, user_verdict: verdict }),
      });
      if (!res.ok) throw new Error("Feedback failed");
      setFeedbackGiven((prev) => ({ ...prev, [rowKey]: verdict }));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="panel">
      <div className="table-header">
        <h2 className="panel__title">Recent Email Scans</h2>
        <div className="table-filters">
          {["all", "phishing", "legitimate", "uncertain"].map((f) => (
            <button
              key={f}
              className={`table-filter ${filter === f ? "table-filter--active" : ""}`}
              onClick={() => setFilter(f)}
            >
              {FILTER_LABELS[f]}
            </button>
          ))}
        </div>
      </div>

      {filtered.length === 0 ? (
        <p className="status-message">No matching scans yet.</p>
      ) : (
        <table className="scans-table">
          <thead>
            <tr>
              <th>Date &amp; Time</th>
              <th>Sender</th>
              <th>Subject</th>
              <th>Risk Level</th>
              <th>Confidence</th>
              <th>Status</th>
              <th>Feedback</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((p) => {
              const date = new Date(p.predicted_at);
              const id = `${p.email_id}-${p.predicted_at}`;
              const expanded = expandedId === id;
              const given = feedbackGiven[id];
              return (
                <React.Fragment key={id}>
                  <tr className="scans-table__row" onClick={() => setExpandedId(expanded ? null : id)}>
                    <td className="muted" data-label="Date">
                      {date.toLocaleDateString(undefined, { month: "short", day: "numeric" })}, {date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    </td>
                    <td className="truncate" data-label="Sender">{p.sender || "(unknown)"}</td>
                    <td className="truncate" data-label="Subject">{p.subject || "(no subject)"}</td>
                    <td data-label="Risk"><RiskBadge level={riskLevel(p)} /></td>
                    <td className="muted" data-label="Confidence">{(p.confidence_score * 100).toFixed(1)}%</td>
                    <td data-label="Status"><StatusBadge label={p.predicted_label} /></td>
                    <td data-label="Feedback">
                      {p.predicted_label === "uncertain" ? (
  <span className="feedback-review">Needs review</span>
) : given ? (
                        <span className="feedback-done">Thanks!</span>
                      ) : (
                        <div className="feedback-btns">
                          <button
                            className="feedback-btn feedback-btn--up"
                            title="Correctly classified"
                            onClick={(e) => submitFeedback(p.email_id, p.predicted_label === "phishing" ? "true_positive" : "true_negative", id, e)}
                          >
                            <ThumbsUp size={13} />
                          </button>
                          <button
                            className="feedback-btn feedback-btn--down"
                            title="Incorrectly classified"
                            onClick={(e) => submitFeedback(p.email_id, p.predicted_label === "phishing" ? "false_positive" : "false_negative", id, e)}
                          >
                            <ThumbsDown size={13} />
                          </button>
                        </div>
                      )}
                    </td>
                    <td data-label=""><Eye size={15} className="view-icon" /></td>
                  </tr>
                  {expanded && (
                    <tr className="scans-table__details-row">
                      <td colSpan={8}>
                        <p className="email-row__snippet">{p.body_snippet}</p>
                        {p.reasons?.length > 0 && (
                          <div className="reasons">{p.reasons.map((r, i) => <span key={i} className="reason-tag">{r}</span>)}</div>
                        )}
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}