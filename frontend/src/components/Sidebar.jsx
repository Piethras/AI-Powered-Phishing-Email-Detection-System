import React from "react";
import { Shield } from "lucide-react";
import { NAV_ITEMS } from "../constants";

export default function Sidebar({ active, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <Shield size={22} className="sidebar__brand-icon" />
        <div>
          <div className="sidebar__brand-name">PhishGuard</div>
          <div className="sidebar__brand-tag">Smarter emails. Safer you.</div>
        </div>
      </div>
      <nav className="sidebar__nav">
        {NAV_ITEMS.map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            className={`sidebar__nav-item ${active === key ? "sidebar__nav-item--active" : ""}`}
            onClick={() => onNavigate(key)}
          >
            <Icon size={17} />
            {label}
          </button>
        ))}
      </nav>
      <div className="sidebar__footer">
        <Shield size={16} />
        <div>
          <div className="sidebar__footer-title">AI-Powered Detection</div>
          <div className="sidebar__footer-text">Header, URL, and language analysis combined into one score.</div>
        </div>
      </div>
    </aside>
  );
}