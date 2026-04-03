import React, { useState } from 'react';
import { useAnalysis } from '../context/AnalysisContext.jsx';

const AnalysisResults = () => {
  const { analysis, isAnalyzing } = useAnalysis();
  const [activeTab, setActiveTab] = useState('transcript');

  if (isAnalyzing) {
    return (
      <div className="glass-card p-12 rounded-xl flex flex-col items-center justify-center gap-4 text-center animate-pulse">
        <span className="material-symbols-outlined text-5xl text-primary animate-spin">cyclone</span>
        <div>
          <h3 className="text-xl font-headline text-white font-bold">Neural Engine Processing...</h3>
          <p className="text-sm text-outline">Transcribing audio and validating SOP via Deepgram Nova-3</p>
        </div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="glass-card p-12 rounded-xl flex flex-col items-center justify-center gap-4 text-center border-dashed border-outline-variant/30">
        <span className="material-symbols-outlined text-5xl text-outline/30">analytics</span>
        <div>
          <h3 className="text-xl font-headline text-white font-bold">No Analysis Data</h3>
          <p className="text-sm text-outline">Upload a Hinglish or Tanglish call recording to see insights.</p>
        </div>
      </div>
    );
  }

  const { transcript, summary, sop_validation, analytics, keywords, language } = analysis;

  const sopSteps = [
    { label: 'Greeting', key: 'greeting' },
    { label: 'Identification', key: 'identification' },
    { label: 'Problem Statement', key: 'problemStatement' },
    { label: 'Solution Offering', key: 'solutionOffering' },
    { label: 'Closing', key: 'closing' },
  ];

  const getSentimentIcon = (s) => {
    if (s === 'Positive') return { icon: 'sentiment_satisfied', color: 'text-tertiary' };
    if (s === 'Negative') return { icon: 'sentiment_dissatisfied', color: 'text-error' };
    return { icon: 'sentiment_neutral', color: 'text-secondary' };
  };

  const sentiment = getSentimentIcon(analytics.sentiment);

  return (
    <section className="space-y-6">
      {/* Top Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <div className="glass-card p-5 rounded-xl flex flex-col gap-2">
          <p className="text-[10px] uppercase tracking-widest text-outline font-bold">Call Sentiment</p>
          <div className="flex items-center justify-between">
            <h3 className={`text-2xl font-bold font-headline ${sentiment.color}`}>{analytics.sentiment}</h3>
            <span className={`material-symbols-outlined ${sentiment.color}`}>{sentiment.icon}</span>
          </div>
        </div>
        
        <div className="glass-card p-5 rounded-xl flex flex-col gap-2">
          <p className="text-[10px] uppercase tracking-widest text-outline font-bold">SOP Compliance</p>
          <div className="flex items-center justify-between">
            <h3 className="text-2xl font-bold font-headline text-white">{Math.round(sop_validation.complianceScore * 100)}%</h3>
            <span className={`material-symbols-outlined ${sop_validation.adherenceStatus === 'FOLLOWED' ? 'text-tertiary' : 'text-error'}`}>
              {sop_validation.adherenceStatus === 'FOLLOWED' ? 'verified_user' : 'warning'}
            </span>
          </div>
        </div>

        <div className="glass-card p-5 rounded-xl flex flex-col gap-2">
          <p className="text-[10px] uppercase tracking-widest text-outline font-bold">Payment Type</p>
          <div className="flex items-center justify-between">
            <h3 className="text-2lg font-bold font-headline text-white truncate max-w-[120px]">{analytics.paymentPreference.replace('_', ' ')}</h3>
            <span className="material-symbols-outlined text-primary">credit_card</span>
          </div>
        </div>

        <div className="glass-card p-5 rounded-xl flex flex-col gap-2">
          <p className="text-[10px] uppercase tracking-widest text-outline font-bold">Rejection Reason</p>
          <div className="flex items-center justify-between">
            <h3 className="text-2lg font-bold font-headline text-white truncate max-w-[120px]">{analytics.rejectionReason.replace('_', ' ')}</h3>
            <span className="material-symbols-outlined text-error">cancel</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Analysis Area */}
        <div className="lg:col-span-2 glass-card p-6 rounded-xl space-y-6">
          <div className="flex items-center justify-between border-b border-outline-variant/10 pb-4">
            <div className="flex gap-4">
              {['transcript', 'summary'].map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`text-sm font-bold uppercase tracking-wider transition-all ${
                    activeTab === tab ? 'text-primary border-b-2 border-primary pb-4 -mb-[17px]' : 'text-outline hover:text-white'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] bg-primary/10 text-primary px-2 py-0.5 rounded font-bold uppercase tracking-tighter">
                {language}
              </span>
            </div>
          </div>

          <div className="min-h-[200px]">
            {activeTab === 'transcript' ? (
              <div className="bg-surface-container-low/40 p-4 rounded-lg border border-outline-variant/10 max-h-[400px] overflow-y-auto custom-scrollbar">
                <p className="text-sm text-on-surface leading-loose whitespace-pre-wrap">
                  {transcript}
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                 <div className="p-4 bg-primary-container/10 border-l-4 border-primary rounded-r-lg">
                    <p className="text-sm text-white italic leading-relaxed">
                      "{summary}"
                    </p>
                 </div>
                 <div className="flex flex-wrap gap-2">
                   {keywords.map(kw => (
                     <span key={kw} className="text-[10px] font-bold px-2 py-1 rounded bg-surface-container-highest text-outline uppercase">
                        #{kw}
                     </span>
                   ))}
                 </div>
              </div>
            )}
          </div>
        </div>

        {/* SOP & Details Sidebar */}
        <div className="space-y-6">
          <div className="glass-card p-6 rounded-xl flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <h4 className="font-headline font-bold text-white uppercase tracking-widest text-xs">SOP Points</h4>
              <span className={`text-[10px] px-2 py-1 rounded font-bold ${sop_validation.adherenceStatus === 'FOLLOWED' ? 'bg-tertiary/20 text-tertiary' : 'bg-error/20 text-error'}`}>
                {sop_validation.adherenceStatus}
              </span>
            </div>
            <div className="space-y-3">
              {sopSteps.map(step => (
                <div key={step.key} className="flex items-center justify-between p-2 rounded bg-surface-container-low/30 border border-outline-variant/5">
                  <span className="text-xs text-outline">{step.label}</span>
                  <span className={`material-symbols-outlined text-sm ${sop_validation[step.key] ? 'text-tertiary' : 'text-outline/30'}`}>
                    {sop_validation[step.key] ? 'check_circle' : 'cancel'}
                  </span>
                </div>
              ))}
            </div>
            <p className="text-[11px] text-outline italic leading-relaxed border-t border-outline-variant/10 pt-3">
              {sop_validation.explanation}
            </p>
          </div>

          <div className="glass-card p-6 rounded-xl bg-gradient-to-br from-surface-variant/40 to-surface-variant/10">
            <h4 className="font-headline font-bold text-white uppercase tracking-widest text-xs mb-4">Business Intel</h4>
            <div className="space-y-4">
                <div>
                   <p className="text-[10px] text-outline uppercase font-bold mb-1">Intent detected</p>
                   {analytics.rejectionReason === 'NONE' ? (
                     <span className="text-xs text-tertiary font-bold flex items-center gap-1">
                        <span className="material-symbols-outlined text-sm">thumb_up</span> High Interest / Lead Qualified
                     </span>
                   ) : (
                     <span className="text-xs text-error font-bold flex items-center gap-1">
                        <span className="material-symbols-outlined text-sm">block</span> Rejection Found
                     </span>
                   )}
                </div>
                <div>
                  <p className="text-[10px] text-outline uppercase font-bold mb-1">Detected payment</p>
                  <span className="text-sm text-white font-headline font-bold">{analytics.paymentPreference.replace('_', ' ')}</span>
                </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AnalysisResults;
