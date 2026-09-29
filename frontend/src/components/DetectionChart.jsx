import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export default function DetectionChart({ dailySeries }) {
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
        <Line type="monotone" dataKey="uncertain" stroke="#E0B85E" strokeWidth={2.5} dot={{ r: 3 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}