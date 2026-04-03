import React, { useEffect, useState } from 'react';
import { fetchDocuments } from '../services/api.js';

const statusColor = (status = '') => {
  const normalized = status.toLowerCase();
  if (normalized.includes('ready') || normalized.includes('done')) return 'bg-tertiary/20 text-tertiary';
  if (normalized.includes('processing') || normalized.includes('running')) return 'bg-primary/15 text-primary';
  if (normalized.includes('error')) return 'bg-error/20 text-error';
  return 'bg-outline-variant/20 text-outline';
};

const DocumentPreview = () => {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const load = async () => {
    try {
      setLoading(true);
      const data = await fetchDocuments();
      if (Array.isArray(data)) {
        const sorted = data.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
        setDocs(sorted);
      }
    } catch (err) {
      setError('Could not fetch documents.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // Auto-refresh every 30 seconds for the dashboard feel
    const interval = setInterval(load, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="glass-card rounded-xl p-6 flex flex-col gap-4">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs uppercase tracking-widest text-outline font-bold">Workspace</p>
          <h3 className="text-xl font-semibold font-headline text-white">Recent uploads</h3>
          {loading && docs.length === 0 && <p className="text-[11px] text-outline animate-pulse mt-1">Fetching latest data...</p>}
        </div>
        <button 
          onClick={load}
          className="p-1.5 rounded-lg bg-surface-container-high text-outline hover:text-white transition-colors"
          title="Refresh"
        >
          <span className="material-symbols-outlined text-sm">refresh</span>
        </button>
      </div>
      
      <div className="space-y-3 max-h-[400px] overflow-y-auto custom-scrollbar pr-1">
        {docs.length > 0 ? (
          docs.map((doc) => (
            <div
              key={doc.id}
              className="flex items-center justify-between bg-surface-container-low/60 border border-outline-variant/10 rounded-lg px-4 py-3 hover:border-primary/30 transition-all cursor-default group"
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-surface-container-highest flex items-center justify-center">
                   <span className="material-symbols-outlined text-sm text-outline group-hover:text-primary transition-colors">
                     {doc.language?.toLowerCase() === 'hindi' ? 'translate' : 'language'}
                   </span>
                </div>
                <div>
                  <p className="text-sm font-semibold text-white truncate max-w-[150px]">{doc.title || `Call #${doc.id}`}</p>
                  <p className="text-[10px] text-outline">{doc.language} Audio • {doc.sentiment}</p>
                </div>
              </div>
              <span className={`px-2.5 py-1 text-[10px] rounded-full font-bold uppercase tracking-tighter ${statusColor(doc.status)}`}>
                {doc.status || 'Ready'}
              </span>
            </div>
          ))
        ) : (
          !loading && (
            <div className="text-center py-8">
              <p className="text-[11px] text-outline italic">No recent analyses found.</p>
              <p className="text-[10px] text-outline/50 mt-1">Upload a call to begin.</p>
            </div>
          )
        )}
      </div>
      
      {docs.length > 0 && (
        <button className="w-full py-2 text-[11px] font-bold text-outline border border-dashed border-outline-variant/30 rounded-lg hover:text-white hover:border-outline-variant/50 transition-all">
          VIEW DATA HISTORY
        </button>
      )}
    </div>
  );
};

export default DocumentPreview;
