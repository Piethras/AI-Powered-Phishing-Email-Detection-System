import React, { useState, useEffect } from "react";
import { Target, AlertTriangle, CheckCircle2, Gauge } from "lucide-react";
import "./App.css";

import { API_BASE } from "./constants";
import Sidebar from "./components/Sidebar";
import MobileNav from "./components/MobileNav";
import TopBar from "./components/TopBar";
import StatCard from "./components/StatCard";
import UploadPanel from "./components/UploadPanel";
import LastResultCard from "./components/LastResultCard";
import DetectionChart from "./components/DetectionChart";
import AccuracyGauge from "./components/AccuracyGauge";
import FlaggedRateDonut from "./components/FlaggedRateDonut";
import RiskDistribution from "./components/RiskDistribution";
import TopDomainsPanel from "./components/TopDomainsPanel";
import ScansTable from "./components/ScansTable";
import QuickPanel from "./components/QuickPanel";
import ScanEmailPage from "./pages/ScanEmailPage";
import WhitelistPage from "./pages/WhitelistPage";
import SettingsPage from "./pages/SettingsPage";

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
        <TopBar predictions={predictions} />

        {activeNav === "scan" ? (
          <ScanEmailPage onScanned={handleUploaded} />
               ) : activeNav === "whitelist" ? (
          <WhitelistPage />
        ) : activeNav === "settings" ? (
          <SettingsPage />
        ) : activeNav !== "dashboard" ? (
          <p className="status-message">This section is coming soon.</p>
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