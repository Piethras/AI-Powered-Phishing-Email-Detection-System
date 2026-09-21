import React from "react";
import { riskLevel } from "../utils";

export default function RiskDistribution({ predictions }) {
  const buckets = { High: 0, Medium: 0, Low: 0 };
  predictions.forEach((p) => { buckets[riskLevel(p)]++; });
  const max = Math.max(...Object.values(buckets), 1);
  const colors = { High: "#EF9494", Medium: "#E0B85E", Low: "#7FD4AC" };
  return (
    <div className="domains-list">
      {Object.entries(buckets).map(([level, count]) => (
        <div key={level} className="domain-row">
          <span className="domain-row__name">{level} risk</span>
          <div className="domain-row__bar-track">
            <div className="domain-row__bar" style={{ width: `${(count / max) * 100}%`, background: colors[level] }} />
          </div>
          <span className="domain-row__count">{count}</span>
        </div>
      ))}
      <p className="risk-note">High: ≥90% confidence · Medium: 70–90% · Low: below threshold (Day 13)</p>
    </div>
  );
}