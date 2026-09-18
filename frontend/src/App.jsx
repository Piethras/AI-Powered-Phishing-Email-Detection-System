import React from "react";
import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { Shield, Mail, History, ListChecks, MessageSquare, Settings, AlertTriangle, CheckCircle2, Target, Inbox, Gauge, Bell, Send, Eye, Menu, X, ThumbsUp, ThumbsDown, Plus } from "lucide-react";
import "./App.css";

const API_BASE = "http://127.0.0.1:5000/api";

const NAV_ITEMS = [
  { key: "dashboard", label: "Dashboard", icon: Shield },
  { key: "scan", label: "Scan Email", icon: Mail },
  { key: "history", label: "Email History", icon: History },
  { key: "whitelist", label: "Whitelist", icon: ListChecks },
  { key: "feedback", label: "Feedback", icon: MessageSquare },
  { key: "settings", label: "Settings", icon: Settings },
];

function Sidebar({ active, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <Shield size={22} className="sidebar__brand-icon" />
        <div>
          <div className="sidebar__brand-name">PhishGuard AI</div>
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

function TopBar() {
  const now = new Date();
  return (
    <div className="topbar">
      <div className="topbar__greeting">
        <h1>Good {now.getHours() < 12 ? "morning" : now.getHours() < 18 ? "afternoon" : "evening"} 👋</h1>
        <p>Your AI assistant for safer emails. Detect, prevent, stay secure.</p>
      </div>
      <div className="topbar__right">
        <span className="topbar__date">
          {now.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" })} &nbsp;·&nbsp;
          {now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </span>
        <button className="topbar__bell"><Bell size={17} /></button>
        <div className="topbar__avatar">U</div>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, accent }) {
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

function UploadPanel({ onUploaded }) {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFile = async (file) => {
    if (!file) return;
    setUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: formData });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Upload failed");
      onUploaded(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div
      className={`upload-panel ${dragActive ? "upload-panel--active" : ""}`}
      onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
      onDragLeave={() => setDragActive(false)}
      onDrop={(e) => { e.preventDefault(); setDragActive(false); handleFile(e.dataTransfer.files[0]); }}
    >
      <Inbox size={20} className="upload-panel__icon" />
      <p className="upload-panel__title">{uploading ? "Scanning email..." : "Drop a .eml file here, or"}</p>
      {!uploading && (
        <label className="upload-panel__button">
          Choose file
          <input type="file" accept=".eml" style={{ display: "none" }} onChange={(e) => handleFile(e.target.files[0])} />
        </label>
      )}
      {error && <p className="upload-panel__error">{error}</p>}
    </div>
  );
}

function LastResultCard({ result, onDismiss }) {
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

function DetectionChart({ dailySeries }) {
  if (!dailySeries || dailySeries.length === 0) {
    return <p className="status-message">Not enough data yet for a trend chart.</p>;
  }
  return (
    <ResponsiveContainer width="100%" height={230}>
      <LineChart data={dailySeries} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#EDF0F4" />
        <XAxis dataKey="date" stroke="#9AA2B1" fontSize={11} />
        <YAxis stroke="#9AA2B1" fontSize={11} allowDecimals={false} />
        <Tooltip contentStyle={{ background: "#fff", border: "1px solid #E4E8EE", borderRadius: 8, fontSize: 12 }} />
        <Line type="monotone" dataKey="legitimate" stroke="#38A874" strokeWidth={2.5} dot={{ r: 3 }} />
        <Line type="monotone" dataKey="phishing" stroke="#E1554F" strokeWidth={2.5} dot={{ r: 3 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}

function AccuracyGauge() {
  const data = [{ value: 98 }, { value: 2 }];
  return (
    <div className="gauge-wrap">
      <div className="gauge-chart-box">
        <ResponsiveContainer width={150} height={150}>
          <PieChart>
            <Pie data={data} innerRadius={52} outerRadius={68} startAngle={90} endAngle={-270} dataKey="value" stroke="none">
              <Cell fill="#7C5CFC" />
              <Cell fill="#EEF0F5" />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="gauge-center">
          <span className="gauge-center__value">98%</span>
          <span className="gauge-center__label">Precision</span>
        </div>
      </div>
    </div>
  );
}

function FlaggedRateDonut({ flagged, legitimate }) {
  const total = flagged + legitimate;
  const rate = total > 0 ? ((flagged / total) * 100).toFixed(1) : "0";
  const data = [{ name: "Phishing", value: flagged }, { name: "Legitimate", value: legitimate }];
  const COLORS = ["#E1554F", "#38A874"];
  return (
    <div className="donut-wrap">
      <div className="donut-chart-box">
        <ResponsiveContainer width={130} height={130}>
          <PieChart>
            <Pie data={data} innerRadius={42} outerRadius={58} paddingAngle={3} dataKey="value" stroke="none">
              {data.map((entry, i) => <Cell key={i} fill={COLORS[i]} />)}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="donut-center">
          <span className="donut-center__value">{rate}%</span>
          <span className="donut-center__label">Flagged</span>
        </div>
      </div>
      <div className="donut-legend">
        <div><span className="dot dot--phishing" />Phishing&nbsp;<strong>{flagged}</strong></div>
        <div><span className="dot dot--legit" />Legitimate&nbsp;<strong>{legitimate}</strong></div>
      </div>
    </div>
  );
}

function riskLevel(p) {
  if (p.predicted_label !== "phishing") return "Low";
  return p.confidence_score >= 0.9 ? "High" : "Medium";
}

function RiskBadge({ level }) {
  return <span className={`badge badge--risk-${level.toLowerCase()}`}>{level}</span>;
}

function StatusBadge({ label }) {
  const isPhishing = label === "phishing";
  return <span className={`badge ${isPhishing ? "badge--phishing" : "badge--legit"}`}>{isPhishing ? "Phishing" : "Legitimate"}</span>;
}

function ScansTable({ predictions }) {
  const [filter, setFilter] = useState("all");
  const [expandedId, setExpandedId] = useState(null);
  const [feedbackGiven, setFeedbackGiven] = useState({});

  const filtered = predictions.filter((p) => {
    if (filter === "phishing") return p.predicted_label === "phishing";
    if (filter === "legitimate") return p.predicted_label !== "phishing";
    return true;
  });

  const submitFeedback = async (emailId, verdict, rowKey, e) => {
    e.stopPropagation();
    try {
      const res = await fetch(`${API_BASE}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email_id: emailId, user_verdict: verdict }),
      });
      if (!res.ok) throw new Error("Feedback failed");
      setFeedbackGiven((prev) => ({ ...prev, [rowKey]: verdict }));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="panel">
      <div className="table-header">
        <h2 className="panel__title">Recent Email Scans</h2>
        <div className="table-filters">
          {["all", "phishing", "legitimate"].map((f) => (
            <button
              key={f}
              className={`table-filter ${filter === f ? "table-filter--active" : ""}`}
              onClick={() => setFilter(f)}
            >
              {f === "all" ? "All" : f === "phishing" ? "Phishing" : "Legitimate"}
            </button>
          ))}
        </div>
      </div>

      {filtered.length === 0 ? (
        <p className="status-message">No matching scans yet.</p>
      ) : (
        <table className="scans-table">
          <thead>
            <tr>
              <th>Date &amp; Time</th>
              <th>Sender</th>
              <th>Subject</th>
              <th>Risk Level</th>
              <th>Confidence</th>
              <th>Status</th>
              <th>Feedback</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((p) => {
              const date = new Date(p.predicted_at);
              const id = `${p.email_id}-${p.predicted_at}`;
              const expanded = expandedId === id;
              const given = feedbackGiven[id];
              return (
                <React.Fragment key={id}>
                  <tr className="scans-table__row" onClick={() => setExpandedId(expanded ? null : id)}>
                    <td className="muted" data-label="Date">
                      {date.toLocaleDateString(undefined, { month: "short", day: "numeric" })}, {date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    </td>
                    <td className="truncate" data-label="Sender">{p.sender || "(unknown)"}</td>
                    <td className="truncate" data-label="Subject">{p.subject || "(no subject)"}</td>
                    <td data-label="Risk"><RiskBadge level={riskLevel(p)} /></td>
                    <td className="muted" data-label="Confidence">{(p.confidence_score * 100).toFixed(1)}%</td>
                    <td data-label="Status"><StatusBadge label={p.predicted_label} /></td>
                    <td data-label="Feedback">
                      {given ? (
                        <span className="feedback-done">Thanks!</span>
                      ) : (
                        <div className="feedback-btns">
                          <button
                            className="feedback-btn feedback-btn--up"
                            title="Correctly classified"
                            onClick={(e) => submitFeedback(p.email_id, p.predicted_label === "phishing" ? "true_positive" : "true_negative", id, e)}
                          >
                            <ThumbsUp size={13} />
                          </button>
                          <button
                            className="feedback-btn feedback-btn--down"
                            title="Incorrectly classified"
                            onClick={(e) => submitFeedback(p.email_id, p.predicted_label === "phishing" ? "false_positive" : "false_negative", id, e)}
                          >
                            <ThumbsDown size={13} />
                          </button>
                        </div>
                      )}
                    </td>
                    <td data-label=""><Eye size={15} className="view-icon" /></td>
                  </tr>
                  {expanded && (
                    <tr className="scans-table__details-row">
                      <td colSpan={8}>
                        <p className="email-row__snippet">{p.body_snippet}</p>
                        {p.reasons?.length > 0 && (
                          <div className="reasons">{p.reasons.map((r, i) => <span key={i} className="reason-tag">{r}</span>)}</div>
                        )}
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}

function TopDomainsPanel({ domains }) {
  if (!domains || domains.length === 0) return <p className="status-message">No flagged domains yet.</p>;
  const max = Math.max(...domains.map((d) => d.count));
  return (
    <div className="domains-list">
      {domains.map((d) => (
        <div key={d.domain} className="domain-row">
          <span className="domain-row__name">{d.domain}</span>
          <div className="domain-row__bar-track">
            <div className="domain-row__bar" style={{ width: `${(d.count / max) * 100}%` }} />
          </div>
          <span className="domain-row__count">{d.count}</span>
        </div>
      ))}
    </div>
  );
}

function QuickPanel({ onNavigate, predictions }) {
  const recent = predictions.slice(0, 5);
  return (
    <div className="quick-panel">
      <button className="quick-panel__scan-btn" onClick={() => onNavigate("scan")}>
        <Send size={15} /> Scan New Email
      </button>
      <button className="quick-panel__secondary-btn" onClick={() => onNavigate("whitelist")}>
        <ListChecks size={15} /> Add to Whitelist
      </button>

      <div className="quick-panel__section">
        <h3>Recent Activity</h3>
        {recent.length === 0 && <p className="status-message">No activity yet.</p>}
        {recent.map((p) => {
          const isPhishing = p.predicted_label === "phishing";
          const date = new Date(p.predicted_at);
          return (
            <div key={`${p.email_id}-${p.predicted_at}`} className="activity-item">
              <span className={`activity-item__dot ${isPhishing ? "activity-item__dot--phishing" : "activity-item__dot--legit"}`}>
                {isPhishing ? <AlertTriangle size={13} /> : <CheckCircle2 size={13} />}
              </span>
              <div>
                <div className="activity-item__title">{isPhishing ? "Phishing detected" : "Marked legitimate"}</div>
                <div className="activity-item__sub">{p.sender || "unknown sender"}</div>
                <div className="activity-item__time">{date.toLocaleDateString()} {date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ScanEmailPage({ onScanned }) {
  const [sender, setSender] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState(null);

  const handleScan = async () => {
    if (!body.trim()) { setError("Email body is required."); return; }
    setScanning(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sender, subject, body }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Scan failed");
      onScanned(data);
      setSender(""); setSubject(""); setBody("");
    } catch (err) {
      setError(err.message);
    } finally {
      setScanning(false);
    }
  };

  return (
    <div className="panel">
      <h2 className="panel__title">Scan an Email Manually</h2>
      <div className="scan-form">
        <input className="scan-form__input" placeholder="Sender (e.g. security@example.com)" value={sender} onChange={(e) => setSender(e.target.value)} />
        <input className="scan-form__input" placeholder="Subject" value={subject} onChange={(e) => setSubject(e.target.value)} />
        <textarea className="scan-form__textarea" placeholder="Paste the email body here..." rows={8} value={body} onChange={(e) => setBody(e.target.value)} />
        {error && <p className="upload-panel__error">{error}</p>}
        <button className="scan-form__submit" onClick={handleScan} disabled={scanning}>
          {scanning ? "Scanning..." : "Scan Email"}
        </button>
      </div>
    </div>
  );
}

function MobileNav({ active, onNavigate }) {
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

function WhitelistPage() {
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

function App() {
  const [predictions, setPredictions] = useState([]);
  const [insights, setInsights] = useState(null);
  const [status, setStatus] = useState("loading");
  const [lastResult, setLastResult] = useState(null);
  const [activeNav, setActiveNav] = useState("dashboard");

  const loadAll = () => {
    setStatus("loading");
    Promise.all([
      fetch(`${API_BASE}/predictions`).then((r) => r.json()),
      fetch(`${API_BASE}/insights`).then((r) => r.json()),
    ])
      .then(([preds, ins]) => { setPredictions(preds); setInsights(ins); setStatus("ready"); })
      .catch(() => setStatus("error"));
  };

  useEffect(() => { loadAll(); }, []);

  const handleUploaded = (result) => { setLastResult(result); loadAll(); };

  return (
    <div className="layout">
      <Sidebar active={activeNav} onNavigate={setActiveNav} />
      <MobileNav active={activeNav} onNavigate={setActiveNav} />
      <div className="app">
        <TopBar />

                {activeNav === "scan" ? (
          <ScanEmailPage onScanned={handleUploaded} />
        ) : activeNav === "whitelist" ? (
          <WhitelistPage />
        ) : activeNav !== "dashboard" ? (
          <p className="status-message">This section is coming soon — Day 19 will wire up more actions.</p>
        ) : (
          <>
            <div className="dashboard-body">
              <div className="dashboard-main">
                {status === "ready" && insights && (
                  <div className="stat-grid">
                    <StatCard icon={Target} label="Total Scanned" value={insights.total_scanned} />
                    <StatCard icon={AlertTriangle} label="Phishing Detected" value={insights.total_flagged} accent="phishing" />
                    <StatCard icon={CheckCircle2} label="Legitimate Emails" value={insights.total_legitimate} accent="legit" />
                    <StatCard icon={Gauge} label="Model Precision" value="98%" accent="purple" />
                  </div>
                )}

                <UploadPanel onUploaded={handleUploaded} />
                {lastResult && <LastResultCard result={lastResult} onDismiss={() => setLastResult(null)} />}

                {status === "ready" && insights && (
                  <div className="panel overview-panel">
                    <h2 className="panel__title">Detection Overview</h2>
                    <div className="overview-panel__body">
                      <DetectionChart dailySeries={insights.daily_series} />
                      <AccuracyGauge />
                    </div>
                  </div>
                )}
              </div>

              <QuickPanel onNavigate={setActiveNav} predictions={predictions} />
            </div>

            {status === "ready" && insights && (
              <div className="panel-grid--2x2" style={{ marginTop: 16 }}>
                <div className="panel">
                  <h2 className="panel__title">Flagged Rate</h2>
                  <FlaggedRateDonut flagged={insights.total_flagged} legitimate={insights.total_legitimate} />
                </div>
                <div className="panel">
                  <h2 className="panel__title">Most Flagged Domains</h2>
                  <TopDomainsPanel domains={insights.top_flagged_domains} />
                </div>
              </div>
            )}

            <main className="main">
              {status === "loading" && <p className="status-message">Loading...</p>}
              {status === "error" && <p className="status-message status-message--error">Could not reach the backend. Is the Flask server running?</p>}
              {status === "ready" && <ScansTable predictions={predictions} />}
            </main>
          </>
        )}
      </div>
    </div>
  );
}

export default App;