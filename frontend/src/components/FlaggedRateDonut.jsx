import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

export default function FlaggedRateDonut({ flagged, legitimate }) {
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