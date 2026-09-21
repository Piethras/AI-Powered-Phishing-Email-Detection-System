import React from "react";

export function RiskBadge({ level }) {
  return <span className={`badge badge--risk-${level.toLowerCase()}`}>{level}</span>;
}

export function StatusBadge({ label }) {
  const isPhishing = label === "phishing";
  return <span className={`badge ${isPhishing ? "badge--phishing" : "badge--legit"}`}>{isPhishing ? "Phishing" : "Legitimate"}</span>;
}