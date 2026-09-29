import React, { useState, useEffect } from "react";
import { RiskBadge, StatusBadge } from "../components/Badges";
import { riskLevel } from "../utils";
import { API_BASE } from "../constants";

const FILTER_LABELS = { all: "All", phishing: "Phishing", legitimate: "Legitimate", uncertain: "Needs Review" };

export default function EmailHistoryPage() {
  const [predictions, setPredictions] = useState([]);
  const [filter, setFilter] = useState("all");
  const [status, setStatus] = useState("loading");
  const [expandedId, setExpandedId] = useState(null);

  const load = (label) => {
    setStatus("loading");
    const url = label && label !== "all" ? `${API_BASE}/predictions/all?label=${label}` : `${API_BASE}/predictions/all`;
    fetch(url)
      .then((r) => r.json())
      .then((data) => { setPredictions(data); setStatus("ready"); })
      .catch(() => setStatus("error"));
  };

  useEffect(() => { load(filter); }, [filter]);

  return (
    <div className="panel">
      <div className="table-header">
        <h2 className="panel__title">Full Email History</h2>
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

      {status === "loading" && <p className="status-message">Loading...</p>}
      {status === "error" && <p className="status-message status-message--error">Could not load history.</p>}
      {status === "ready" && predictions.length === 0 && <p className="status-message">No emails scanned yet.</p>}

      {status === "ready" && predictions.length > 0 && (
        <>
          <p className="status-message" style={{ marginBottom: 12 }}>{predictions.length} total record{predictions.length !== 1 ? "s" : ""}</p>
          <table className="scans-table">
            <thead>
              <tr>
                <th>Date &amp; Time</th>
                <th>Sender</th>
                <th>Subject</th>
                <th>Risk Level</th>
                <th>Confidence</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map((p) => {
                const date = new Date(p.predicted_at);
                const id = `${p.email_id}-${p.predicted_at}`;
                const expanded = expandedId === id;
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
                    </tr>
                    {expanded && (
                      <tr className="scans-table__details-row">
                        <td colSpan={6}>
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
        </>
      )}
    </div>
  );
}