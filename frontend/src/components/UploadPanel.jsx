import React, { useState } from "react";
import { Inbox } from "lucide-react";
import { API_BASE } from "../constants";

export default function UploadPanel({ onUploaded }) {
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