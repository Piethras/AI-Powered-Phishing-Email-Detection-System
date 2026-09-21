import React, { useState } from "react";
import { Bell, AlertTriangle } from "lucide-react";

export default function TopBar({ predictions }) {
  const now = new Date();
  const [showNotifs, setShowNotifs] = useState(false);
  const recentPhishing = predictions.filter((p) => p.predicted_label === "phishing").slice(0, 5);

  return (
    <div className="topbar">
      <div className="topbar__row">
        <div className="topbar__greeting">
          <h1>Good {now.getHours() < 12 ? "morning" : now.getHours() < 18 ? "afternoon" : "evening"} 👋</h1>
          <p>Your AI assistant for safer emails. Detect, prevent, stay secure.</p>
        </div>
        <div className="topbar__icons">
          <div className="topbar__notif-wrap">
            <button className="topbar__bell" onClick={() => setShowNotifs(!showNotifs)}>
              <Bell size={17} />
              {recentPhishing.length > 0 && <span className="topbar__bell-dot" />}
            </button>
            {showNotifs && (
              <>
                <div className="topbar__notif-backdrop" onClick={() => setShowNotifs(false)} />
                <div className="topbar__notif-dropdown">
                  <div className="topbar__notif-header">Recent Alerts</div>
                  {recentPhishing.length === 0 ? (
                    <p className="status-message" style={{ padding: "12px 16px" }}>No recent alerts.</p>
                  ) : (
                    recentPhishing.map((p) => (
                      <div key={`${p.email_id}-${p.predicted_at}`} className="topbar__notif-item">
                        <AlertTriangle size={14} className="topbar__notif-icon" />
                        <div>
                          <div className="topbar__notif-title">Phishing detected</div>
                          <div className="topbar__notif-sub">{p.sender || "unknown sender"}</div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </>
            )}
          </div>
          <div className="topbar__avatar">U</div>
        </div>
      </div>
      <span className="topbar__date">
        {now.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" })} &nbsp;·&nbsp;
        {now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
      </span>
    </div>
  );
}