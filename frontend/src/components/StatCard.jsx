import React from "react";

export default function StatCard({ icon: Icon, label, value, accent }) {
  return (
    <div className="stat-card">
      <div className={`stat-card__icon stat-card__icon--${accent || "default"}`}>
        <Icon size={19} />
      </div>
      <div>
        <span className="stat-card__label">{label}</span>
        <span className="stat-card__value">{value}</span>
      </div>
    </div>
  );
}