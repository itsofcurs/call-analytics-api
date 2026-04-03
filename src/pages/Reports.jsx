import React, { useEffect, useState } from 'react';
import { fetchAnalysis } from '../services/api.js';

const Reports = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let ignore = false;
    const load = async () => {
      try {
        setLoading(true);
        const result = await fetchAnalysis();
        if (!ignore) setData(result);
      } catch (err) {
        if (!ignore) setError('Could not load reports yet.');
      } finally {
        if (!ignore) setLoading(false);
      }
    };
    load();
    return () => {
      ignore = true;
    };
  }, []);

  return (
    <div className="space-y-4">
      <div className="glass-card rounded-xl p-6 space-y-3">
        <p className="text-xs uppercase tracking-widest text-outline font-bold">Reports</p>
        <h3 className="text-xl font-semibold font-headline text-white">Compliance & sentiment</h3>
        {loading && <p className="text-sm text-outline">Loading…</p>}
        {error && <p className="text-sm text-error">{error}</p>}
        {data && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm text-on-surface">
            <div className="p-4 rounded-lg bg-surface-container-low/60 border border-outline-variant/10">
              <p className="text-[11px] text-outline">Summary</p>
              <p className="font-semibold text-white">{data.summary || '—'}</p>
            </div>
            <div className="p-4 rounded-lg bg-surface-container-low/60 border border-outline-variant/10">
              <p className="text-[11px] text-outline">Sentiment</p>
              <p className="font-semibold text-white">{data.sentiment || '—'}</p>
            </div>
            <div className="p-4 rounded-lg bg-surface-container-low/60 border border-outline-variant/10">
              <p className="text-[11px] text-outline">SOP coverage</p>
              <p className="font-semibold text-white">{data.sop_score ? `${Math.round(data.sop_score * 100)}%` : '—'}</p>
            </div>
          </div>
        )}
        {!loading && !data && !error && (
          <p className="text-sm text-outline">No aggregates yet. Trigger some analyses to see data.</p>
        )}
      </div>
    </div>
  );
};

export default Reports;
