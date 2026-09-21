import React, { useState } from "react";
import { Shield, Menu, X } from "lucide-react";
import { NAV_ITEMS } from "../constants";

export default function MobileNav({ active, onNavigate }) {
  const [open, setOpen] = useState(false);

  const handleSelect = (key) => {
    onNavigate(key);
    setOpen(false);
  };

  return (
    <div className="mobile-nav">
      <button className="mobile-nav__toggle" onClick={() => setOpen(!open)}>
        {open ? <X size={20} /> : <Menu size={20} />}
      </button>
      {open && (
        <>
          <div className="mobile-nav__backdrop" onClick={() => setOpen(false)} />
          <div className="mobile-nav__drawer">
            <div className="mobile-nav__brand">
              <Shield size={20} className="sidebar__brand-icon" />
              <span>PhishGuard AI</span>
            </div>
            {NAV_ITEMS.map(({ key, label, icon: Icon }) => (
              <button
                key={key}
                className={`mobile-nav__item ${active === key ? "mobile-nav__item--active" : ""}`}
                onClick={() => handleSelect(key)}
              >
                <Icon size={17} />
                {label}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}