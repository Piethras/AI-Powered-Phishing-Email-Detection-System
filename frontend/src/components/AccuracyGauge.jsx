import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

export default function AccuracyGauge() {
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