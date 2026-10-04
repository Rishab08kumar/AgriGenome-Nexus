import { useState, useEffect, useRef } from 'react';
import { getLatestSensorData } from '../services/api';

// Generate realistic mock sensor reading with drift
const generateMockReading = (prev) => {
  const drift = (val, range, min, max) => {
    const change = (Math.random() - 0.5) * range;
    return Math.min(max, Math.max(min, val + change));
  };
  return {
    soil_moisture:   drift(prev?.soil_moisture   ?? 55,  2,  10, 95),
    temperature:     drift(prev?.temperature     ?? 28,  0.4, 15, 42),
    humidity:        drift(prev?.humidity        ?? 65,  1.5, 30, 95),
    light_intensity: drift(prev?.light_intensity ?? 45000, 2000, 0, 100000),
    nitrogen:        drift(prev?.nitrogen        ?? 120,  3,  20, 400),
    phosphorus:      drift(prev?.phosphorus      ?? 45,   1.5, 5, 100),
    potassium:       drift(prev?.potassium       ?? 180,  2.5, 30, 350),
    ec:              drift(prev?.ec              ?? 1.2,  0.05, 0.1, 4.0),
    ph:              null,   // sensor not connected
    weight:          null,
    timestamp:       new Date().toISOString(),
  };
};

/**
 * useFirebase — real-time sensor data hook.
 *
 * Behaviour:
 *  1. Tries to fetch from GET /api/sensor-data/latest every 5 seconds.
 *  2. Falls back to simulated drift data if the API is unreachable.
 *  3. Exposes `isLive` flag so the UI can indicate connectivity state.
 */
const useFirebase = () => {
  const [sensorData, setSensorData] = useState(null);
  const [history, setHistory] = useState([]);   // last 24-pt rolling window
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isLive, setIsLive] = useState(false);

  const prevRef = useRef(null);

  const fetchData = async () => {
    try {
      const res = await getLatestSensorData();
      const data = res.data;
      setSensorData(data);
      prevRef.current = data;
      setIsLive(true);
      setError(null);
    } catch {
      // Backend not running — use simulated drift
      setIsLive(false);
      const simulated = generateMockReading(prevRef.current);
      prevRef.current = simulated;
      setSensorData(simulated);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(); // initial fetch

    // Real-time poll every 5 seconds
    const interval = setInterval(async () => {
      await fetchData();
      // Keep rolling 24-point history for charts
      setHistory((h) => {
        const entry = {
          ...prevRef.current,
          t: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }),
        };
        const updated = [...h, entry];
        return updated.slice(-24);
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return { sensorData, history, loading, error, isLive };
};

export default useFirebase;
