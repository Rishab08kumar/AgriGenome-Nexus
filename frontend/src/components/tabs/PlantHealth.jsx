import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Leaf, UploadCloud, AlertTriangle, CheckCircle, Bug, Zap, Activity } from 'lucide-react';
import StatusBadge from '../ui/StatusBadge';
import { motion, AnimatePresence } from 'framer-motion';
import { detectPlantHealth } from '../../services/api';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const HEALTH_CONFIG = {
  'Healthy': {
    color: '#00ff88',
    icon: CheckCircle,
    status: 'healthy',
    action: 'Plant is thriving. Continue current irrigation and nutrient schedule.',
    bgClass: 'bg-agri-green/10 border-agri-green/30',
    textClass: 'text-agri-green',
  },
  'Pest Infestation': {
    color: '#ff4444',
    icon: Bug,
    status: 'critical',
    action: 'Apply recommended pesticide treatment. Isolate affected plants and increase monitoring frequency.',
    bgClass: 'bg-red-500/10 border-red-500/30',
    textClass: 'text-red-400',
  },
  'Nutrient Deficiency': {
    color: '#ffd700',
    icon: AlertTriangle,
    status: 'warning',
    action: 'Increase nutrient dosing in next fertigation cycle. Consider foliar spray for faster uptake.',
    bgClass: 'bg-yellow-500/10 border-yellow-500/30',
    textClass: 'text-yellow-400',
  },
  'Phenotypic Anomaly': {
    color: '#ff6622',
    icon: Zap,
    status: 'critical',
    action: 'Unusual growth pattern detected. Consult agronomist. Check for environmental stress or genetic issues.',
    bgClass: 'bg-orange-500/10 border-orange-500/30',
    textClass: 'text-orange-400',
  },
};

const RECENT_SCANS = [
  { date: 'Today, 09:41 AM', label: 'Healthy', status: 'healthy', confidence: 97 },
  { date: 'Yesterday, 14:20 PM', label: 'Pest Infestation', status: 'critical', confidence: 83 },
  { date: 'Oct 01, 11:15 AM', label: 'Healthy', status: 'healthy', confidence: 95 },
  { date: 'Sep 30, 08:30 AM', label: 'Nutrient Deficiency', status: 'warning', confidence: 76 },
];

const PlantHealth = () => {
  const [image, setImage] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setImage(URL.createObjectURL(file));
    setImageFile(file);
    setAnalyzing(true);
    setResult(null);
    setError(null);

    try {
      const res = await detectPlantHealth(file);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      // Demo fallback
      const demoLabels = ['Healthy', 'Nutrient Deficiency', 'Pest Infestation', 'Phenotypic Anomaly'];
      const label = demoLabels[Math.floor(Math.random() * demoLabels.length)];
      setResult({
        label,
        confidence: 0.72 + Math.random() * 0.26,
        bounding_boxes: [{ x: 80, y: 60, width: 200, height: 180, label, conf: 0.85 }],
      });
      setError('Backend offline — showing demo analysis.');
    } finally {
      setAnalyzing(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpg', '.jpeg', '.png', '.webp'] },
    multiple: false,
    maxSize: 10 * 1024 * 1024,
  });

  const config = result ? (HEALTH_CONFIG[result.label] || HEALTH_CONFIG['Healthy']) : null;
  const confidencePct = result ? Math.round(result.confidence * 100) : 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-2 bg-agri-green/10 rounded-lg">
          <Leaf className="w-5 h-5 text-agri-green" />
        </div>
        <div>
          <h2 className="text-xl font-rajdhani font-bold text-gray-100">Plant Health Vision AI</h2>
          <p className="text-xs text-gray-500">MobileNetV2 + YOLOv8 — PlantVillage trained</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* ── Upload Zone ── */}
        <div className="space-y-4">
          <div
            {...getRootProps()}
            className={`glass-card relative border-2 rounded-2xl min-h-[400px] flex flex-col items-center justify-center cursor-pointer transition-all duration-300 overflow-hidden
              ${isDragActive
                ? 'border-agri-green bg-agri-green/10 scale-[1.02]'
                : image
                  ? 'border-transparent p-0'
                  : 'border-dashed border-gray-700 hover:border-agri-green/50 hover:bg-agri-green/5 p-8 text-center'
              }`}
          >
            <input {...getInputProps()} />

            {image ? (
              <div className="relative w-full h-full min-h-[400px]">
                <img
                  src={image}
                  alt="Uploaded leaf"
                  className="absolute inset-0 w-full h-full object-cover rounded-2xl"
                />

                {/* Scan line animation */}
                <AnimatePresence>
                  {analyzing && (
                    <>
                      <div className="absolute inset-0 bg-black/50 backdrop-blur-[2px] rounded-2xl" />
                      <motion.div
                        className="absolute left-0 right-0 h-0.5 bg-agri-glow z-10"
                        style={{ boxShadow: '0 0 20px #39ff14, 0 0 40px #39ff14' }}
                        animate={{ top: ['0%', '100%', '0%'] }}
                        transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
                      />
                      <div className="absolute inset-0 flex items-center justify-center z-20">
                        <div className="bg-black/80 px-6 py-3 rounded-full border border-agri-glow flex items-center gap-3">
                          <Activity className="w-4 h-4 text-agri-glow animate-pulse" />
                          <span className="text-agri-glow font-rajdhani text-lg tracking-widest">ANALYZING...</span>
                        </div>
                      </div>
                    </>
                  )}
                </AnimatePresence>

                {/* Bounding boxes */}
                <AnimatePresence>
                  {result && result.bounding_boxes?.map((box, i) => {
                    const boxColor = config?.color || '#00ff88';
                    return (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="absolute rounded pointer-events-none"
                        style={{
                          left: `${(box.x / 400) * 100}%`,
                          top: `${(box.y / 400) * 100}%`,
                          width: `${(box.width / 400) * 100}%`,
                          height: `${(box.height / 400) * 100}%`,
                          border: `2px solid ${boxColor}`,
                          boxShadow: `0 0 12px ${boxColor}88`,
                          background: `${boxColor}11`,
                        }}
                      >
                        <div
                          className="absolute -top-6 left-0 text-xs px-2 py-0.5 rounded font-bold"
                          style={{ background: boxColor + 'dd', color: '#000' }}
                        >
                          {box.label} {Math.round((box.conf || result.confidence) * 100)}%
                        </div>
                      </motion.div>
                    );
                  })}
                </AnimatePresence>

                {/* Re-upload overlay */}
                {!analyzing && (
                  <div className="absolute bottom-3 right-3 z-20">
                    <div className="bg-black/70 text-xs text-gray-400 px-3 py-1.5 rounded-full border border-gray-600 hover:border-agri-green transition-colors">
                      Click to re-upload
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <>
                <div className="p-5 rounded-full bg-agri-green/10 border border-agri-green/20 mb-4">
                  <UploadCloud className="w-12 h-12 text-agri-green" />
                </div>
                <h3 className="text-xl font-rajdhani text-gray-200 mb-2">
                  {isDragActive ? 'Drop leaf image here...' : 'Drag & Drop Leaf Image'}
                </h3>
                <p className="text-sm text-gray-500">or click to browse from device / ESP32-CAM feed</p>
                <div className="mt-6 text-xs text-gray-600 uppercase tracking-widest border border-gray-800 px-4 py-1.5 rounded-full">
                  JPG · PNG · WebP · Max 10MB
                </div>
              </>
            )}
          </div>
        </div>

        {/* ── Results Panel ── */}
        <div className="space-y-5">
          <div className="glass-card p-6 rounded-xl border border-gray-700/50 min-h-[220px]">
            <h3 className="text-lg font-rajdhani text-gray-300 mb-4 border-b border-gray-800 pb-2 flex items-center gap-2">
              <Activity className="w-4 h-4" /> Analysis Results
            </h3>

            <AnimatePresence mode="wait">
              {!image ? (
                <motion.div key="empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  className="text-gray-600 flex flex-col items-center justify-center h-28 gap-2">
                  <Leaf className="w-8 h-8 opacity-20" />
                  <p className="text-sm">Upload a leaf image to start analysis</p>
                </motion.div>
              ) : analyzing ? (
                <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  className="space-y-3 animate-pulse">
                  <div className="h-4 bg-gray-800 rounded w-1/3" />
                  <div className="h-8 bg-gray-800 rounded w-2/3" />
                  <div className="h-4 bg-gray-800 rounded w-1/2" />
                  <div className="h-16 bg-gray-800 rounded" />
                </motion.div>
              ) : result && config ? (
                <motion.div key="result" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4 }} className="space-y-4">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <StatusBadge status={config.status} text={config.status.toUpperCase()} />
                      <h4 className={`text-xl font-bold mt-2 ${config.textClass}`}>{result.label}</h4>
                    </div>
                    <div className="w-20 h-20 shrink-0">
                      <CircularProgressbar
                        value={confidencePct}
                        text={`${confidencePct}%`}
                        styles={buildStyles({
                          textColor: config.color,
                          pathColor: config.color,
                          trailColor: 'rgba(255,255,255,0.05)',
                          textSize: '22px',
                        })}
                      />
                    </div>
                  </div>

                  <div className={`border rounded-lg p-3 flex gap-3 ${config.bgClass}`}>
                    <config.icon className={`w-4 h-4 shrink-0 mt-0.5 ${config.textClass}`} />
                    <div>
                      <div className={`font-semibold text-xs mb-1 uppercase tracking-wider ${config.textClass}`}>
                        Recommended Action
                      </div>
                      <div className="text-gray-300 text-sm">{config.action}</div>
                    </div>
                  </div>

                  {error && (
                    <div className="text-xs text-yellow-600 bg-yellow-500/5 border border-yellow-500/20 rounded px-3 py-2">
                      ⚠️ {error}
                    </div>
                  )}
                </motion.div>
              ) : null}
            </AnimatePresence>
          </div>

          {/* Recent Scans */}
          <div className="glass-card p-6 rounded-xl border border-gray-700/50">
            <h3 className="text-lg font-rajdhani text-gray-300 mb-4 border-b border-gray-800 pb-2">
              📋 Recent Scans
            </h3>
            <div className="space-y-2">
              {RECENT_SCANS.map((scan, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.08 }}
                  className="flex items-center justify-between p-2.5 hover:bg-gray-800/40 rounded-lg transition-colors"
                >
                  <span className="text-sm text-gray-500">{scan.date}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-gray-600">{scan.confidence}%</span>
                    <StatusBadge status={scan.status} text={scan.label} />
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlantHealth;
