import React from "react";

export default function LastResultCard({ result, onDismiss }) {
  const kind = result.label === "phishing" ? "phishing" : result.label === "uncertain" ? "uncertain" : "legit";
  const headline = kind === "uncertain" ? "Review" : `${(result.final_score * 100).toFixed(0)}%`;
  const text = { phishing: "Flagged as Phishing", uncertain: "Needs human review", legit: "Looks Legitimate" }[kind];
  return (
    <div className={`result-card result-card--${kind}`}>
      <div className="result-card__header">
        <span className="result-card__score">{headline}</span>
        <span className="result-card__label">{text}</span>
        <button className="result-card__dismiss" onClick={onDismiss}>×</button>
      </div>
      {result.reasons?.length > 0 && (
        <div className="reasons">{result.reasons.map((r, i) => <span key={i} className="reason-tag">{r}</span>)}</div>
      )}
      {kind !== "uncertain" && (
        <div className="result-card__scores">
          <span>text: {(result.specialist_scores.text * 100).toFixed(0)}%</span>
          <span>header: {(result.specialist_scores.header * 100).toFixed(0)}%</span>
          <span>url: {(result.specialist_scores.url * 100).toFixed(0)}%</span>
        </div>
      )}
    </div>
  );
}