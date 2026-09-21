import React, { useState, useEffect } from "react";
import { Plus } from "lucide-react";
import { API_BASE } from "../constants";

export default function WhitelistPage() {
  const [entries, setEntries] = useState([]);
  const [domain, setDomain] = useState("");
  const [addedBy, setAddedBy] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = () => {
    fetch(`${API_BASE}/whitelist`)
      .then((r) => r.json())
      .then((data) => { setEntries(data); setLoading(false); })
      .catch(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleAdd = async () => {
    if (!domain.trim()) { setError("Domain is required."); return; }
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/whitelist`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sender_domain: domain.trim(), added_by: addedBy.trim() || "unknown" }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed to add");
      setDomain("");
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="panel">
      <h2 className="panel__title">Whitelisted Senders</h2>
      <p className="status-message" style={{ marginBottom: 16 }}>
        Emails from whitelisted domains are automatically classified as legitimate,
        skipping full analysis. Add domains deliberately &mdash; this is a separate,
        intentional action from routine scan feedback.
      </p>

      <div className="whitelist-form">
        <input className="scan-form__input" placeholder="Domain (e.g. company.com)" value={domain} onChange={(e) => setDomain(e.target.value)} />
        <input className="scan-form__input" placeholder="Your name" value={addedBy} onChange={(e) => setAddedBy(e.target.value)} />
        <button className="scan-form__submit" onClick={handleAdd}><Plus size={14} /> Add</button>
      </div>
      {error && <p className="upload-panel__error">{error}</p>}

      {loading ? (
        <p className="status-message">Loading...</p>
      ) : entries.length === 0 ? (
        <p className="status-message">No domains whitelisted yet.</p>
      ) : (
        <table className="scans-table" style={{ marginTop: 20 }}>
          <thead>
            <tr><th>Domain</th><th>Added By</th><th>Added At</th></tr>
          </thead>
          <tbody>
            {entries.map((w) => (
              <tr key={w.id}>
                <td>{w.sender_domain}</td>
                <td className="muted">{w.added_by}</td>
                <td className="muted">{new Date(w.added_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}