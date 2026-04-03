import axios from 'axios';

const API_KEY = import.meta.env.VITE_API_KEY || 'sk_track3_987654321';
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({ 
  baseURL: API_BASE_URL,
  headers: {
    'x-api-key': API_KEY
  }
});

/**
 * Converts a File object to Base64 string
 */
export const fileToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
};

/**
 * Main Track 3 Call Analysis Endpoint
 */
export async function analyzeCall(file, language = "Hindi") {
  const b64 = await fileToBase64(file);
  const audioFormat = file.name.split('.').pop() || 'mp3';
  
  const payload = {
    language: language,
    audioFormat: audioFormat,
    audioBase64: b64
  };

  const { data } = await api.post('/analyze-call', payload);
  return data;
}

export async function analyzeDocument(file) {
  const formData = new FormData();
  formData.append('file', file);

  const { data } = await api.post('/analyze-document', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

  return data;
}

export async function fetchAnalysis() {
  const { data } = await api.get('/analysis');
  return data;
}

export async function fetchDocuments() {
  const { data } = await api.get('/documents');
  return data;
}
