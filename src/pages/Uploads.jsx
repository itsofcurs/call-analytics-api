import React from 'react';
import FileUpload from '../components/FileUpload.jsx';
import DocumentPreview from '../components/DocumentPreview.jsx';

const Uploads = () => (
  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <FileUpload />
    <div className="space-y-4">
      <DocumentPreview />
      <div className="glass-card rounded-xl p-6">
        <p className="text-xs uppercase tracking-widest text-outline font-bold">How it works</p>
        <h3 className="text-xl font-semibold font-headline text-white mb-2">Async analysis</h3>
        <p className="text-sm text-outline leading-relaxed">
          Documents queue into the Celery worker, run OCR ➜ summarizer ➜ sentiment ➜ SOP validation. Use the API client to
          poll job status or upload here for a quick check.
        </p>
      </div>
    </div>
  </div>
);

export default Uploads;
