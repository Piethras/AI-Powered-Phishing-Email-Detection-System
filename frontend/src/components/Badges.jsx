import React from "react";

const STATUS = {
  phishing: { text: "Phishing", cls: "badge--phishing" },
  legitimate: { text: "Legitimate", cls: "badge--legit" },
  uncertain: { text: "Needs Review", cls: "badge--uncertain" },
};

export function RiskBadge({ level }) {
  return <span className={`badge badge--risk-${level.toLowerCase()}`}>{level}</span>;
}

export function StatusBadge({ label }) {
  const s = STATUS[label] || STATUS.uncertain;
  return <span className={`badge ${s.cls}`}>{s.text}</span>;
}