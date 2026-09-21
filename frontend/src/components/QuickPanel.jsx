import React from "react";
import { Send, ListChecks, AlertTriangle, CheckCircle2 } from "lucide-react";

export default function QuickPanel({ onNavigate, predictions }) {
  const recent = predictions.slice(0, 5);
  return (
    <div className="quick-panel">
      <button className="quick-panel__scan-btn" onClick={() => onNavigate("scan")}>
        <Send size={15} /> Scan New Email
      </button>
      <button className="quick-panel__secondary-btn" onClick={() => onNavigate("whitelist")}>
        <ListChecks size={15} /> Add to Whitelist
      </button>

      <div className="quick-panel__section">
        <h3>Recent Activity</h3>
        {recent.length === 0 && <p className="status-message">No activity yet.</p>}
        {recent.map((p) => {
          const isPhishing = p.predicted_label === "phishing";
          const date = new Date(p.predicted_at);
          return (
            <div key={`${p.email_id}-${p.predicted_at}`} className="activity-item">
              <span className={`activity-item__dot ${isPhishing ? "activity-item__dot--phishing" : "activity-item__dot--legit"}`}>
                {isPhishing ? <AlertTriangle size={13} /> : <CheckCircle2 size={13} />}
              </span>
              <div>
                <div className="activity-item__title">{isPhishing ? "Phishing detected" : "Marked legitimate"}</div>
                <div className="activity-item__sub">{p.sender || "unknown sender"}</div>
                <div className="activity-item__time">{date.toLocaleDateString()} {date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}