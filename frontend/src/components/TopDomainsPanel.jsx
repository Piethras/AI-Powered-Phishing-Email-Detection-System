import React from "react";

export default function TopDomainsPanel({ domains }) {
  if (!domains || domains.length === 0) return <p className="status-message">No flagged domains yet.</p>;
  const max = Math.max(...domains.map((d) => d.count));
  return (
    <div className="domains-list">
      {domains.map((d) => (
        <div key={d.domain} className="domain-row">
          <span className="domain-row__name">{d.domain}</span>
          <div className="domain-row__bar-track">
            <div className="domain-row__bar" style={{ width: `${(d.count / max) * 100}%` }} />
          </div>
          <span className="domain-row__count">{d.count}</span>
        </div>
      ))}
    </div>
  );
}