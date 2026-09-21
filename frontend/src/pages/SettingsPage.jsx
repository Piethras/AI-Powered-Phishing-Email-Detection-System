import React, { useState, useEffect } from "react";
import { API_BASE } from "../constants";

export default function SettingsPage() {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/system-info`)
      .then((r) => r.json())
      .then(setInfo)
      .catch(() => setInfo(null));
  }, []);

  return (
    <div className="panel">
      <h2 className="panel__title">System Settings</h2>
      {!info ? (
        <p className="status-message">Loading system info...</p>
      ) : (
        <div className="settings-list">
          <div className="settings-row">
            <span className="settings-row__label">Model Version</span>
            <span className="settings-row__value">{info.model_version}</span>
          </div>
          <div className="settings-row">
            <span className="settings-row__label">Decision Threshold</span>
            <span className="settings-row__value">{(info.threshold * 100).toFixed(0)}%</span>
          </div>
          <div className="settings-row">
            <span className="settings-row__label">Specialist Modules</span>
            <span className="settings-row__value">{info.specialists.join(", ")}</span>
          </div>
          <div className="settings-row">
            <span className="settings-row__label">Database</span>
            <span className="settings-row__value">{info.database}</span>
          </div>
          <div className="settings-row">
            <span className="settings-row__label">Total Emails Scanned</span>
            <span className="settings-row__value">{info.total_emails_in_db}</span>
          </div>
          <div className="settings-row">
            <span className="settings-row__label">Whitelisted Domains</span>
            <span className="settings-row__value">{info.whitelisted_domains}</span>
          </div>
        </div>
      )}
    </div>
  );
}