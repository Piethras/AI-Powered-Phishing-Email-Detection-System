export function riskLevel(p) {
  if (p.predicted_label !== "phishing") return "Low";
  return p.confidence_score >= 0.9 ? "High" : "Medium";
}