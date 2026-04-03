import React, { useEffect, useState } from 'react';
import { analyzeCall, analyzeDocument } from '../services/api.js';
import { useAnalysis } from '../context/AnalysisContext.jsx';

const ACCEPTED_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/msword',
  'audio/mpeg',
  'audio/wav',
  'audio/mp3',
  'audio/x-wav'
];

const FileUpload = () => {
  const { setAnalysis, setIsAnalyzing } = useAnalysis();
  const [file, setFile] = useState(null);
  const [language, setLanguage] = useState('Hindi');
  const [previewUrl, setPreviewUrl] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [resultMessage, setResultMessage] = useState('');

  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const isImage = (input) => input && input.type?.startsWith('image/');
  const isAudio = (input) => input && input.type?.startsWith('audio/');

  const validateFile = (input) => {
    if (!input) return false;
    const isAcceptedType = ACCEPTED_TYPES.includes(input.type) || isImage(input);
    if (!isAcceptedType) {
      setError('Allowed: PDF, DOCX, Images, Audio (MP3/WAV).');
      return false;
    }
    setError('');
    return true;
  };

  const handleFiles = (input) => {
    const selected = Array.isArray(input) ? input[0] : input;
    if (!validateFile(selected)) return;
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(isImage(selected) ? URL.createObjectURL(selected) : '');
    setFile(selected);
    setResultMessage('');
  };

  const onInputChange = (event) => {
    const selected = event.target.files?.[0];
    if (selected) handleFiles(selected);
  };

  const onDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    const selected = event.dataTransfer.files?.[0];
    if (selected) handleFiles(selected);
  };

  const onDragOver = (event) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = () => setIsDragging(false);

  const handleUpload = async () => {
    if (!file) return;
    try {
      setLoading(true);
      setIsAnalyzing(true);
      setError('');
      setResultMessage('');
      
      let data;
      if (isAudio(file)) {
        data = await analyzeCall(file, language);
      } else {
        data = await analyzeDocument(file);
      }
      
      if (data.status === 'success' || data.status === 200) {
        setAnalysis(data);
        setResultMessage('Analysis completed successfully.');
      } else {
        setError(data.message || 'Analysis failed.');
      }
    } catch (err) {
      setError(err?.response?.data?.message || 'Processing failed. Please check backend connection.');
    } finally {
      setLoading(false);
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="glass-card rounded-xl p-6 flex flex-col gap-4">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs uppercase tracking-widest text-outline font-bold">Process Call</p>
          <h3 className="text-xl font-semibold font-headline text-white">Multilingual Analysis</h3>
          <p className="text-sm text-outline mt-1">Upload audio for Hinglish/Tanglish STT & SOP checks.</p>
        </div>
        <span className="material-symbols-outlined text-primary bg-primary/10 p-2 rounded-lg">clinical_notes</span>
      </div>

      <div className="flex gap-2">
        {['Hindi', 'Tamil'].map(lang => (
          <button
            key={lang}
            onClick={() => setLanguage(lang)}
            className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
              language === lang ? 'bg-primary text-white shadow-lg' : 'bg-surface-container-high text-outline'
            }`}
          >
            {lang}
          </button>
        ))}
      </div>

      <label
        htmlFor="file-input"
        className={`border-2 border-dashed rounded-xl p-6 bg-surface-container-low/50 transition-colors cursor-pointer ${
          isDragging ? 'border-primary bg-primary/5' : 'border-outline-variant/30'
        }`}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
      >
        <input
          id="file-input"
          type="file"
          className="hidden"
          accept=".pdf,.doc,.docx,image/*,audio/*"
          onChange={onInputChange}
        />
        <div className="flex flex-col items-center gap-3 text-center">
          <span className="material-symbols-outlined text-3xl text-primary">
            {file ? (isAudio(file) ? 'audio_file' : 'description') : 'upload_file'}
          </span>
          <p className="text-sm text-outline">
            Drag & drop audio here or <span className="text-primary font-semibold">browse</span>
          </p>
          <button
            type="button"
            onClick={() => document.getElementById('file-input')?.click()}
            className="px-4 py-2 rounded-lg bg-primary-container text-white font-semibold shadow-lg shadow-primary-container/30"
          >
            Select file
          </button>
          <p className="text-[11px] text-outline">Supported: MP3, WAV, PDF, DOCX • Max 50MB</p>
        </div>
      </label>

      {file && (
        <div className="flex items-center gap-4 bg-surface-container-low/60 border border-outline-variant/10 rounded-lg px-4 py-3">
          {isImage(file) && previewUrl ? (
            <img src={previewUrl} alt={file.name} className="w-12 h-12 object-cover rounded" />
          ) : (
            <span className={`material-symbols-outlined text-3xl ${isAudio(file) ? 'text-tertiary' : 'text-secondary'}`}>
              {isAudio(file) ? 'mic' : 'description'}
            </span>
          )}
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-white truncate">{file.name}</p>
            <p className="text-[11px] text-outline">{(file.size / 1024 / 1024).toFixed(2)} MB • {language}</p>
          </div>
          <button
            type="button"
            className="px-3 py-1.5 text-xs rounded-full bg-primary-container text-white font-semibold shadow-lg shadow-primary-container/20 disabled:opacity-50"
            onClick={handleUpload}
            disabled={loading}
          >
            {loading ? 'Processing...' : 'Run Analysis'}
          </button>
        </div>
      )}

      {(error || resultMessage) && (
        <div
          className={`rounded-lg px-4 py-3 text-sm border ${
            error ? 'border-error/40 text-error bg-error/5' : 'border-tertiary/30 text-tertiary bg-tertiary/5'
          }`}
        >
          {error || resultMessage}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
