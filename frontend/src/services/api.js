import axios from 'axios';

// Base URL auto-proxied by Vite (vite.config.js proxy) in dev
// In production, set VITE_API_BASE_URL env variable
const baseURL = import.meta.env.VITE_API_BASE_URL
  ? `${import.meta.env.VITE_API_BASE_URL}/api`
  : '/api';

const api = axios.create({
  baseURL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

// ── Sensor Data ───────────────────────────────────────────────────────────────
export const postSensorData = (data) =>
  api.post('/sensor-data', data);

export const getLatestSensorData = () =>
  api.get('/sensor-data/latest');

// ── Crop Intelligence ─────────────────────────────────────────────────────────
export const recommendCrop = (data) =>
  api.post('/recommend-crop', data);

// ── Dosing Decision ───────────────────────────────────────────────────────────
export const getDosingDecision = (data) =>
  api.post('/dosing-decision', data);

// ── Plant Health (multipart image upload) ─────────────────────────────────────
export const detectPlantHealth = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/plant-health', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000, // image inference can be slow
  });
};

// ── Harvest Readiness ─────────────────────────────────────────────────────────
export const getHarvestReadiness = (data) =>
  api.post('/harvest-readiness', data);

// ── Market Price ──────────────────────────────────────────────────────────────
export const getMarketPrice = (data) =>
  api.post('/market-price', data);

export default api;
