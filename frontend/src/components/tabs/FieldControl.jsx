import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Settings, Power, Droplets, AlertTriangle, CheckCircle } from 'lucide-react';
import StatusBadge from '../ui/StatusBadge';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// ── 3D FARM MAP (pure canvas, no external lib needed) ─────────────
const FarmMap3D = ({ pumpActive, valveOpen, sensorData }) => {
  const canvasRef = useRef(null);
  const animRef   = useRef(null);
  const timeRef   = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width  = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    const W = canvas.width;
    const H = canvas.height;

    // sensor nodes positions (isometric grid)
    const nodes = [
      { x: 0.25, y: 0.35, label: 'Node A', active: true },
      { x: 0.50, y: 0.25, label: 'Node B', active: true },
      { x: 0.75, y: 0.35, label: 'Node C', active: false },
      { x: 0.35, y: 0.60, label: 'Node D', active: true },
      { x: 0.65, y: 0.60, label: 'Node E', active: true },
    ];

    const toIso = (gx, gy) => ({
      x: W * 0.5 + (gx - gy) * W * 0.25,
      y: H * 0.3  + (gx + gy) * H * 0.15,
    });

    const draw = (t) => {
      ctx.clearRect(0, 0, W, H);

      // ── background gradient ──
      const bg = ctx.createLinearGradient(0, 0, 0, H);
      bg.addColorStop(0, '#0a1628');
      bg.addColorStop(1, '#0d2010');
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, W, H);

      // ── isometric ground grid ──
      ctx.strokeStyle = 'rgba(0,255,136,0.08)';
      ctx.lineWidth = 1;
      for (let i = 0; i <= 4; i++) {
        const a = toIso(i, 0), b = toIso(i, 4);
        const c = toIso(0, i), d = toIso(4, i);
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(c.x, c.y); ctx.lineTo(d.x, d.y); ctx.stroke();
      }

      // ── irrigation pipes (lines between nodes) ──
      const pipes = [[0,1],[1,2],[0,3],[1,4],[2,4],[3,4]];
      pipes.forEach(([a, b]) => {
        const na = nodes[a], nb = nodes[b];
        const pa = toIso(na.x * 4, na.y * 4);
        const pb = toIso(nb.x * 4, nb.y * 4);
        ctx.strokeStyle = pumpActive
          ? `rgba(0,180,255,${0.3 + 0.2 * Math.sin(t * 0.05 + a)})`
          : 'rgba(100,100,100,0.2)';
        ctx.lineWidth = pumpActive ? 2 : 1;
        ctx.setLineDash(pumpActive ? [6, 4] : []);
        ctx.lineDashOffset = pumpActive ? -(t * 0.5) : 0;
        ctx.beginPath(); ctx.moveTo(pa.x, pa.y); ctx.lineTo(pb.x, pb.y); ctx.stroke();
        ctx.setLineDash([]);
      });

      // ── sensor nodes ──
      nodes.forEach((node, i) => {
        const p = toIso(node.x * 4, node.y * 4);
        const pulse = 1 + 0.15 * Math.sin(t * 0.05 + i);
        const color = node.active ? '#00ff88' : '#555';

        // glow
        if (node.active) {
          const glow = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 28 * pulse);
          glow.addColorStop(0, 'rgba(0,255,136,0.25)');
          glow.addColorStop(1, 'rgba(0,255,136,0)');
          ctx.fillStyle = glow;
          ctx.beginPath();
          ctx.arc(p.x, p.y, 28 * pulse, 0, Math.PI * 2);
          ctx.fill();
        }

        // node circle
        ctx.fillStyle   = color;
        ctx.strokeStyle = node.active ? 'rgba(0,255,136,0.8)' : '#333';
        ctx.lineWidth   = 2;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 8, 0, Math.PI * 2);
        ctx.fill(); ctx.stroke();

        // label
        ctx.fillStyle = '#ccc';
        ctx.font = '11px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(node.label, p.x, p.y - 15);
      });

      // ── pump indicator (center) ──
      const center = toIso(2, 2);
      const pumpColor = pumpActive ? '#00ff88' : '#555';
      const pumpPulse = pumpActive ? 1 + 0.2 * Math.sin(t * 0.08) : 1;

      if (pumpActive) {
        const pg = ctx.createRadialGradient(center.x, center.y, 0, center.x, center.y, 40 * pumpPulse);
        pg.addColorStop(0, 'rgba(0,255,136,0.3)');
        pg.addColorStop(1, 'rgba(0,255,136,0)');
        ctx.fillStyle = pg;
        ctx.beginPath(); ctx.arc(center.x, center.y, 40 * pumpPulse, 0, Math.PI * 2); ctx.fill();
      }

      ctx.fillStyle   = pumpColor;
      ctx.strokeStyle = pumpActive ? '#00ff88' : '#444';
      ctx.lineWidth   = 3;
      ctx.beginPath(); ctx.arc(center.x, center.y, 14, 0, Math.PI * 2);
      ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#000';
      ctx.font = 'bold 10px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('PUMP', center.x, center.y + 4);

      // ── valve indicator ──
      const valvePos = toIso(3.2, 1.5);
      ctx.fillStyle   = valveOpen ? '#00b4ff' : '#555';
      ctx.strokeStyle = valveOpen ? '#00b4ff' : '#444';
      ctx.lineWidth   = 2;
      ctx.beginPath(); ctx.arc(valvePos.x, valvePos.y, 10, 0, Math.PI * 2);
      ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#000';
      ctx.font = 'bold 9px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('V-A', valvePos.x, valvePos.y + 3);

      // ── moisture heatmap overlay ──
      const moisture = sensorData?.soil_moisture ?? 50;
      const alpha = (moisture / 100) * 0.15;
      ctx.fillStyle = `rgba(0,180,255,${alpha})`;
      ctx.fillRect(0, 0, W, H);

      // ── legend ──
      ctx.font = '11px monospace';
      ctx.textAlign = 'left';
      [
        { color: '#00ff88', text: `Pump: ${pumpActive ? 'ON' : 'OFF'}` },
        { color: '#00b4ff', text: `Valve A: ${valveOpen ? 'OPEN' : 'CLOSED'}` },
        { color: '#fbbf24', text: `Moisture: ${moisture.toFixed(1)}%` },
      ].forEach((item, i) => {
        ctx.fillStyle = item.color;
        ctx.fillRect(12, 12 + i * 18, 10, 10);
        ctx.fillStyle = '#ccc';
        ctx.fillText(item.text, 28, 21 + i * 18);
      });

      animRef.current = requestAnimationFrame(() => {
        timeRef.current += 1;
        draw(timeRef.current);
      });
    };

    draw(0);
    return () => cancelAnimationFrame(animRef.current);
  }, [pumpActive, valveOpen, sensorData]);

  return (
    <canvas
      ref={canvasRef}
      className="w-full h-full"
      style={{ minHeight: '300px' }}
    />
  );
};

// ── MAIN COMPONENT ────────────────────────────────────────────────
const FieldControl = () => {
  const [dosingData,  setDosingData]  = useState(null);
  const [sensorData,  setSensorData]  = useState(null);
  const [loading,     setLoading]     = useState(true);
  const [error,       setError]       = useState(null);
  const [manualPump,  setManualPump]  = useState(null); // null = auto
  const [manualValve, setManualValve] = useState(null); // null = auto
  const [lastUpdated, setLastUpdated] = useState(null);

  // ── fetch dosing decision from backend ──────────────────────────
  const fetchDosing = async () => {
    try {
      // 1. get latest sensor data
      const sRes = await fetch(`${API}/api/sensor-data/latest`);
      const sData = sRes.ok ? await sRes.json() : null;
      if (sData) setSensorData(sData);

      // 2. get dosing decision
      const payload = {
        soil_moisture: sData?.soil_moisture ?? 35,
        N:             sData?.N             ?? 80,
        P:             sData?.P             ?? 20,
        K:             sData?.K             ?? 80,
        ec:            sData?.ec            ?? 1.0,
        ph:            sData?.ph            ?? null,
        crop_variety:  sData?.crop_variety  ?? 'Rose',
      };

      const dRes = await fetch(`${API}/api/dosing-decision`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(payload),
      });

      if (!dRes.ok) throw new Error(`Dosing API ${dRes.status}`);
      const dData = await dRes.json();
      setDosingData(dData);
      setLastUpdated(new Date());
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDosing();
    const interval = setInterval(fetchDosing, 15000); // refresh every 15s
    return () => clearInterval(interval);
  }, []);

  // ── effective states: manual override wins, else auto from backend
  const pumpActive = manualPump  !== null ? manualPump  : (dosingData?.pump_on    ?? false);
  const valveOpen  = manualValve !== null ? manualValve : (dosingData?.valve_open ?? false);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Settings className="w-6 h-6 text-agri-blue" />
          <h2 className="text-2xl font-rajdhani font-bold text-gray-200">Autonomous Field Control</h2>
        </div>
        <div className="flex items-center gap-2 text-xs text-gray-500">
          {loading && <span className="animate-pulse text-agri-green">Syncing...</span>}
          {error   && <span className="text-red-400">⚠ {error}</span>}
          {lastUpdated && !loading && (
            <span>Updated {lastUpdated.toLocaleTimeString()}</span>
          )}
          <button
            onClick={fetchDosing}
            className="px-3 py-1 rounded bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-600"
          >
            Refresh
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        {/* ── PUMP CARD ── */}
        <div className={`glass-card p-6 rounded-xl border flex flex-col items-center justify-center gap-4 transition-all duration-300
          ${pumpActive ? 'border-agri-green shadow-[0_0_15px_rgba(0,255,136,0.2)]' : 'border-gray-700'}`}>
          <div className="text-lg text-gray-300">Main Irrigation Pump</div>
          {manualPump !== null && (
            <span className="text-xs text-yellow-400 border border-yellow-600 px-2 py-0.5 rounded">Manual Override</span>
          )}
          <motion.div
            animate={{ rotate: pumpActive ? 360 : 0 }}
            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
            className={`p-4 rounded-full ${pumpActive ? 'bg-agri-green/20 text-agri-green' : 'bg-gray-800 text-gray-500'}`}
          >
            <Power className="w-12 h-12" />
          </motion.div>

          {/* auto decision badge */}
          {dosingData && (
            <div className="text-xs text-center text-gray-400">
              AI says: <span className={dosingData.pump_on ? 'text-agri-green font-bold' : 'text-gray-500'}>
                {dosingData.pump_on ? '🟢 PUMP ON' : '⚫ PUMP OFF'}
              </span>
            </div>
          )}

          <div className="flex gap-2">
            <button
              onClick={() => setManualPump(!pumpActive)}
              className={`px-4 py-2 rounded-full font-bold uppercase tracking-wide transition-colors text-sm
                ${pumpActive ? 'bg-agri-green text-black' : 'bg-gray-700 text-white'}`}
            >
              {pumpActive ? 'ON' : 'OFF'}
            </button>
            {manualPump !== null && (
              <button
                onClick={() => setManualPump(null)}
                className="px-3 py-2 rounded-full text-xs bg-gray-800 text-gray-400 border border-gray-600 hover:border-agri-green"
              >
                Auto
              </button>
            )}
          </div>
        </div>

        {/* ── VALVE CARD ── */}
        <div className={`glass-card p-6 rounded-xl border flex flex-col items-center justify-center gap-4 transition-all duration-300
          ${valveOpen ? 'border-agri-blue shadow-[0_0_15px_rgba(0,180,255,0.2)]' : 'border-gray-700'}`}>
          <div className="text-lg text-gray-300">Nutrient Valve A</div>
          {manualValve !== null && (
            <span className="text-xs text-yellow-400 border border-yellow-600 px-2 py-0.5 rounded">Manual Override</span>
          )}
          <div className={`p-4 rounded-full transition-colors ${valveOpen ? 'bg-agri-blue/20 text-agri-blue' : 'bg-gray-800 text-gray-500'}`}>
            <Droplets className={`w-12 h-12 ${valveOpen ? 'animate-bounce' : ''}`} />
          </div>

          {/* auto decision badge */}
          {dosingData && (
            <div className="text-xs text-center text-gray-400">
              AI says: <span className={dosingData.valve_open ? 'text-agri-blue font-bold' : 'text-gray-500'}>
                {dosingData.valve_open ? '🔵 VALVE OPEN' : '⚫ VALVE CLOSED'}
              </span>
              {dosingData.nutrient_dose_ml > 0 && (
                <div className="text-agri-gold mt-1">Dose: {dosingData.nutrient_dose_ml}ml</div>
              )}
            </div>
          )}

          <div className="flex gap-2">
            <button
              onClick={() => setManualValve(!valveOpen)}
              className={`px-4 py-2 rounded-full font-bold uppercase tracking-wide transition-colors text-sm
                ${valveOpen ? 'bg-agri-blue text-black' : 'bg-gray-700 text-white'}`}
            >
              {valveOpen ? 'OPEN' : 'CLOSED'}
            </button>
            {manualValve !== null && (
              <button
                onClick={() => setManualValve(null)}
                className="px-3 py-2 rounded-full text-xs bg-gray-800 text-gray-400 border border-gray-600 hover:border-agri-blue"
              >
                Auto
              </button>
            )}
          </div>
        </div>

        {/* ── SYSTEM STATUS CARD ── */}
        <div className="glass-card p-6 rounded-xl border border-gray-700 flex flex-col justify-center">
          <h3 className="text-lg text-gray-300 mb-4">System Status</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Network</span>
              <StatusBadge status={error ? 'error' : 'active'} text={error ? 'Offline' : 'Online'} />
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">AI Status</span>
              <StatusBadge status={dosingData ? 'active' : 'loading'} text={dosingData ? 'Active' : 'Loading'} />
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Nutrient Dose</span>
              <span className="text-agri-gold font-bold">
                {dosingData ? `${dosingData.nutrient_dose_ml}ml` : '—'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Crop Matched</span>
              <span className="text-gray-200 text-sm">
                {dosingData?.matched_species ?? '—'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">EC Level</span>
              <span className={`text-sm font-bold ${
                sensorData?.ec > 2.0 ? 'text-red-400' : 'text-agri-green'
              }`}>
                {sensorData?.ec ? `${sensorData.ec.toFixed(2)} dS/m` : '—'}
              </span>
            </div>
          </div>

          {/* reasons list */}
          {dosingData?.reasons?.length > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-700">
              <div className="text-xs text-gray-500 mb-2">AI Decisions:</div>
              {dosingData.reasons.map((r, i) => (
                <div key={i} className="text-xs text-agri-green flex gap-1 mb-1">
                  <CheckCircle className="w-3 h-3 mt-0.5 shrink-0" />
                  <span>{r}</span>
                </div>
              ))}
            </div>
          )}

          {/* warnings */}
          {dosingData?.warnings?.length > 0 && (
            <div className="mt-2">
              {dosingData.warnings.map((w, i) => (
                <div key={i} className="text-xs text-yellow-400 flex gap-1 mb-1">
                  <AlertTriangle className="w-3 h-3 mt-0.5 shrink-0" />
                  <span>{w}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ── 3D FARM MAP ── */}
      <div className="glass-card rounded-xl border border-gray-700 overflow-hidden">
        <div className="flex items-center justify-between px-6 py-3 border-b border-gray-700">
          <h3 className="text-gray-300 font-rajdhani font-bold">Live 3D Farm Map</h3>
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <span className="w-2 h-2 rounded-full bg-agri-green animate-pulse inline-block" />
            Real-time sensor positions
          </div>
        </div>
        <div style={{ height: '320px' }}>
          <FarmMap3D
            pumpActive={pumpActive}
            valveOpen={valveOpen}
            sensorData={sensorData}
          />
        </div>
      </div>
    </div>
  );
};

export default FieldControl;