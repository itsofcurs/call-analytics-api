import React, { useEffect, useState } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line
} from 'recharts';
import { fetchDocuments } from '../services/api';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const Analytics = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const docs = await fetchDocuments();
        setData(docs);
      } catch (error) {
        console.error("Failed to load analytics", error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  // Data processing for charts
  const sentimentStats = data.reduce((acc, curr) => {
    const s = curr.sentiment || 'neutral';
    acc[s] = (acc[s] || 0) + 1;
    return acc;
  }, {});

  const sentimentChartData = Object.keys(sentimentStats).map(k => ({ name: k, value: sentimentStats[k] }));

  const sopTrendData = data.map((d, index) => ({
    name: `Call ${index + 1}`,
    score: (d.sop_score || 0) * 100
  })).slice(-10); // Last 10 calls

  if (loading) return <div className="p-8 text-outline">Analyzing call history...</div>;

  return (
    <div className="space-y-6 p-4">
      <header className="space-y-1">
        <h2 className="text-2xl font-bold font-headline text-white">Call Center Intelligence</h2>
        <p className="text-outline text-sm">Visualizing performance across all analyzed recordings.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Sentiment Distribution */}
        <div className="glass-card p-6 rounded-2xl border border-outline-variant/10">
          <h3 className="text-lg font-semibold mb-4 text-white">Sentiment Distribution</h3>
          <div className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={sentimentChartData}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {sentimentChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* SOP Compliance Trend */}
        <div className="glass-card p-6 rounded-2xl border border-outline-variant/10">
          <h3 className="text-lg font-semibold mb-4 text-white">SOP Compliance Trend (%)</h3>
          <div className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={sopTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="name" stroke="#666" />
                <YAxis stroke="#666" />
                <Tooltip contentStyle={{ backgroundColor: '#111', border: 'none' }} />
                <Line type="monotone" dataKey="score" stroke="#00C49F" strokeWidth={3} dot={{ r: 5 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
