import React from 'react';
import AnalysisResults from '../components/AnalysisResults.jsx';
import FileUpload from '../components/FileUpload.jsx';

const Home = () => (
  <div className="space-y-8">
    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-outline-variant/10 pb-6">
      <div>
        <h1 className="text-3xl font-black text-white font-headline tracking-tighter uppercase">Call Analytics Console</h1>
        <p className="text-sm text-outline">Intelligent Hinglish & Tanglish Processing Engine</p>
      </div>
      <div className="flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-tertiary animate-pulse shadow-[0_0_8px_#4cd7f6]" />
        <span className="text-[10px] font-bold text-outline uppercase tracking-widest">Active Neural Link</span>
      </div>
    </div>
    
    <div className="grid grid-cols-1 xl:grid-cols-4 gap-8 items-start">
      <div className="xl:col-span-3">
        <AnalysisResults />
      </div>
      <div className="xl:col-span-1 space-y-8">
        <FileUpload />
        
        <div className="glass-card p-6 rounded-xl border-l-4 border-primary shadow-lg shadow-primary/5">
          <p className="text-[10px] uppercase tracking-widest text-outline font-bold mb-3">Hackathon Task</p>
          <ul className="space-y-3">
             {[
               { icon: 'mic', text: 'Voice-to-Text (Hinglish/Tanglish)' },
               { icon: 'summarize', text: 'AI Summarization' },
               { icon: 'verified', text: 'SOP Script Validation' },
               { icon: 'payments', text: 'Payment Categorization' },
               { icon: 'block', text: 'Rejection Analysis' }
             ].map((task, i) => (
                <li key={i} className="flex items-center gap-3 text-[11px] font-medium text-white/80">
                  <span className="material-symbols-outlined text-sm text-primary">{task.icon}</span>
                  {task.text}
                </li>
             ))}
          </ul>
        </div>
      </div>
    </div>
  </div>
);

export default Home;
