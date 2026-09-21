import React from "react";

export default function LastResultCard({ result, onDismiss }) {
  const isPhishing = result.label === "phishing";
  return (
    <div className={`result-card ${isPhishing ? "result-card--phishing" : "result-card--legit"}`}>
      <div className="result-card__header">
        <span className="result-card__score">{(result.final_score * 100).toFixed(0)}%</span>
        <span className="result-card__label">{isPhishing ? "Flagged as Phishing" : "Looks Legitimate"}</span>
        <button className="result-card__dismiss" onClick={onDismiss}>×</button>
      </div>
      {result.reasons?.length > 0 && (
        <div className="reasons">{result.reasons.map((r, i) => <span key={i} className="reason-tag">{r}</span>)}</div>
      )}
      <div className="result-card__scores">
        <span>text: {(result.specialist_scores.text * 100).toFixed(0)}%</span>
        <span>header: {(result.specialist_scores.header * 100).toFixed(0)}%</span>
        <span>url: {(result.specialist_scores.url * 100).toFixed(0)}%</span>
      </div>
    </div>
  );
}