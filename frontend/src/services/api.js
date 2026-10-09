
import axios from 'axios';

// Base URL auto-proxied by Vite in development.
// In production, set VITE_API_BASE_URL to your backend URL.
const backendURL = (
  import.meta.env.VITE_API_BASE_URL || ''
).replace(/\/$/, '');

const baseURL = backendURL
  ? `${backendURL}/api`
  : '/api';

const api = axios.create({
  baseURL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

// ── Sensor Data ──────────────────────────────────────────
export const postSensorData = (data) =>
  api.post('/sensor-data', data);

export const getLatestSensorData = () =>
  api.get('/sensor-data/latest');

// ── Crop Intelligence ────────────────────────────────────
export const recommendCrop = (data) =>
  api.post('/recommend-crop', data);

// ── Dosing Decision ──────────────────────────────────────
export const getDosingDecision = (data) =>
  api.post('/dosing-decision', data);

// ── Plant Health ─────────────────────────────────────────
export const detectPlantHealth = (file) => {
  const formData = new FormData();
  formData.append('file', file);

  return api.post('/plant-health', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000,
  });
};

// ── Harvest Readiness ────────────────────────────────────
export const getHarvestReadiness = (data) =>
  api.post('/harvest-readiness', data);

// ── Market Price ─────────────────────────────────────────
export const getMarketPrice = (data) =>
  api.post('/market-price', data);

// ── NEW: Geo-Adaptive Crop Suitability ───────────────────
// Current FastAPI route: POST /geo-crop-suitability
// This uses the same backend but without the /api prefix.
export const getGeoCropSuitability = (data) =>
  axios.post(
    `${backendURL}/geo-crop-suitability`,
    data,
    {
      timeout: 30000,
      headers: { 'Content-Type': 'application/json' },
    }
  );

export default api;
