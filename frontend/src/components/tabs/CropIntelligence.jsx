import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Dna, Database, MapPin, Thermometer, Droplets, Wind, Sun, FlaskConical, Zap, Info } from 'lucide-react';
import GlowButton from '../ui/GlowButton';
import { recommendCrop } from '../../services/api';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const InputField = ({ label, name, value, onChange, type = 'number', disabled = false, placeholder, tooltip }) => (
  <div className="space-y-1 group relative">
    <label className={`text-xs font-medium uppercase tracking-widest ${disabled ? 'text-gray-600' : 'text-gray-400'}`}>
      {label}
    </label>
    <div className="relative">
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        disabled={disabled}
        placeholder={placeholder}
        step="any"
        className={`w-full rounded-lg px-3 py-2.5 text-sm transition-all duration-200 outline-none
          ${disabled
            ? 'bg-black/20 border border-dashed border-gray-700 text-gray-600 cursor-not-allowed'
            : 'bg-black/40 border border-agri-green/30 text-white focus:border-agri-green focus:ring-1 focus:ring-agri-green/40 hover:border-agri-green/50'
          }`}
      />
      {tooltip && (
        <div className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity z-20">
          <div className="relative">
            <Info className="w-4 h-4 text-gray-600" />
            <div className="absolute right-0 bottom-6 bg-gray-900 text-xs text-gray-300 px-3 py-2 rounded-lg border border-gray-700 w-52 pointer-events-none shadow-xl">
              {tooltip}
            </div>
          </div>
        </div>
      )}
    </div>
  </div>
);

const INITIAL_FORM = {
  latitude: '28.6139',
  longitude: '77.2090',
  soil_moisture: '55',
  temperature: '28',
  humidity: '65',
  light_intensity: '45000',
  nitrogen: '120',
  phosphorus: '45',
  potassium: '180',
  ec: '1.2',
  ph: '',   // always null — sensor not connected
};

const CROP_COLORS = {
  'Rice IR64': '#00b4ff',
  'Wheat HD-2967': '#ffd700',
  'Tomato H-86': '#ff4444',
  'Cotton MCU-5': '#ffffff',
  'Maize DHM-117': '#ffaa00',
  'Soybean JS-335': '#88cc00',
  'Groundnut TAG-24': '#cc8844',
  'Sugarcane CO-86032': '#00ff88',
  'Banana Grand Naine': '#ffdd44',
  'Pepper Panniyur-1': '#ff6622',
};

const CropIntelligence = () => {
  const [form, setForm] = useState(INITIAL_FORM);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const payload = {
      latitude: parseFloat(form.latitude),
      longitude: parseFloat(form.longitude),
      soil_moisture: parseFloat(form.soil_moisture),
      temperature: parseFloat(form.temperature),
      humidity: parseFloat(form.humidity),
      light_intensity: parseFloat(form.light_intensity),
      nitrogen: parseFloat(form.nitrogen),
      phosphorus: parseFloat(form.phosphorus),
      potassium: parseFloat(form.potassium),
      ec: parseFloat(form.ec),
      ph: null, // pH sensor not connected
    };

    try {
      const res = await recommendCrop(payload);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      // Demo fallback so dashboard looks alive even without backend
      setResult({
        crop_variety: 'Wheat HD-2967',
        genomic_strain: 'High-yield Wheat HD-2967',
        confidence: 0.87,
      });
      setError('Backend offline — showing demo result.');
    } finally {
      setLoading(false);
    }
  };

  const cropColor = result ? (CROP_COLORS[result.crop_variety] || '#00ff88') : '#00ff88';
  const confidencePct = result ? Math.round(result.confidence * 100) : 0;

  return (
    <div className="relative min-h-[70vh] flex flex-col md:flex-row gap-8">
      {/* Animated DNA background */}
      <div className="absolute right-0 top-0 opacity-5 pointer-events-none overflow-hidden h-full w-64 flex items-center justify-center">
        <Dna className="w-64 h-64 text-agri-green" style={{ animation: 'spin 20s linear infinite' }} />
      </div>

      {/* ── Input Form ── */}
      <div className="w-full md:w-1/2 glass-card p-8 rounded-2xl relative z-10 border border-agri-green/20">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-agri-blue/10 rounded-lg">
            <Database className="w-5 h-5 text-agri-blue" />
          </div>
          <div>
            <h2 className="text-xl font-rajdhani font-bold text-gray-100">AI Crop Recommendation</h2>
            <p className="text-xs text-gray-500">Genomic strain matching via Random Forest</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Location */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <MapPin className="w-4 h-4 text-agri-blue" />
              <span className="text-xs uppercase tracking-widest text-gray-400">GPS Coordinates</span>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <InputField label="Latitude" name="latitude" value={form.latitude} onChange={handleChange} type="text" />
              <InputField label="Longitude" name="longitude" value={form.longitude} onChange={handleChange} type="text" />
            </div>
          </div>

          {/* Climate */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Thermometer className="w-4 h-4 text-agri-gold" />
              <span className="text-xs uppercase tracking-widest text-gray-400">Climate Sensors</span>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <InputField label="Soil Moisture (%)" name="soil_moisture" value={form.soil_moisture} onChange={handleChange} />
              <InputField label="Temperature (°C)" name="temperature" value={form.temperature} onChange={handleChange} />
              <InputField label="Humidity (% RH)" name="humidity" value={form.humidity} onChange={handleChange} />
              <InputField label="Light (lux)" name="light_intensity" value={form.light_intensity} onChange={handleChange} />
            </div>
          </div>

          {/* NPK + EC */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <FlaskConical className="w-4 h-4 text-agri-green" />
              <span className="text-xs uppercase tracking-widest text-gray-400">Soil Nutrients</span>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <InputField label="Nitrogen N (mg/kg)" name="nitrogen" value={form.nitrogen} onChange={handleChange} />
              <InputField label="Phosphorus P (mg/kg)" name="phosphorus" value={form.phosphorus} onChange={handleChange} />
              <InputField label="Potassium K (mg/kg)" name="potassium" value={form.potassium} onChange={handleChange} />
              <InputField label="EC (mS/cm)" name="ec" value={form.ec} onChange={handleChange} />
            </div>
          </div>

          {/* pH — disabled, future sensor */}
          <InputField
            label="Soil pH"
            name="ph"
            value="Sensor Not Connected"
            onChange={() => {}}
            type="text"
            disabled
            tooltip="pH sensor integration coming soon. Will enhance recommendation accuracy when connected."
          />

          {error && (
            <div className="text-xs text-yellow-500 bg-yellow-500/10 border border-yellow-500/30 rounded-lg px-3 py-2">
              ⚠️ {error}
            </div>
          )}

          <GlowButton type="submit" loading={loading} className="w-full mt-2">
            🧬 Run Genomic Analysis
          </GlowButton>
        </form>
      </div>

      {/* ── Result Card ── */}
      <div className="w-full md:w-1/2 flex items-center justify-center min-h-[400px]">
        <AnimatePresence mode="wait">
          {result ? (
            <motion.div
              key="result"
              initial={{ rotateY: 90, opacity: 0 }}
              animate={{ rotateY: 0, opacity: 1 }}
              exit={{ rotateY: -90, opacity: 0 }}
              transition={{ duration: 0.6, type: 'spring', stiffness: 200 }}
              className="glass-card p-8 rounded-2xl w-full max-w-sm text-center relative border"
              style={{ borderColor: cropColor + '55' }}
            >
              {/* Spinning DNA badge */}
              <div
                className="absolute -top-5 left-1/2 -translate-x-1/2 p-3 rounded-full border"
                style={{ background: '#0a0f0a', borderColor: cropColor }}
              >
                <Dna className="w-6 h-6" style={{ color: cropColor, animation: 'spin 4s linear infinite' }} />
              </div>

              <div className="mt-4">
                <p className="text-xs uppercase tracking-widest text-gray-500 mb-1">Recommended Crop</p>
                <h2 className="text-2xl font-rajdhani font-bold mb-1" style={{ color: cropColor }}>
                  {result.crop_variety}
                </h2>
                <p className="text-sm text-gray-400 italic mb-6">{result.genomic_strain}</p>
              </div>

              <div className="w-36 h-36 mx-auto mb-4">
                <CircularProgressbar
                  value={confidencePct}
                  text={`${confidencePct}%`}
                  styles={buildStyles({
                    textColor: cropColor,
                    pathColor: cropColor,
                    trailColor: 'rgba(255,255,255,0.05)',
                    textSize: '20px',
                  })}
                />
              </div>
              <p className="text-sm text-gray-400">Model Confidence</p>

              <div className="mt-6 grid grid-cols-3 gap-2 text-xs text-gray-500">
                <div className="bg-black/30 rounded-lg p-2">
                  <div className="text-agri-green font-bold">N:{form.nitrogen}</div>
                  <div>mg/kg</div>
                </div>
                <div className="bg-black/30 rounded-lg p-2">
                  <div className="text-agri-blue font-bold">P:{form.phosphorus}</div>
                  <div>mg/kg</div>
                </div>
                <div className="bg-black/30 rounded-lg p-2">
                  <div className="text-agri-gold font-bold">K:{form.potassium}</div>
                  <div>mg/kg</div>
                </div>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="empty"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="text-gray-600 flex flex-col items-center gap-4"
            >
              <div className="w-24 h-24 rounded-full border-2 border-dashed border-gray-700 flex items-center justify-center">
                <Database className="w-10 h-10 opacity-30" />
              </div>
              <p className="font-rajdhani text-xl">Enter field data to get recommendation</p>
              <p className="text-xs text-gray-700">AI will suggest the best crop & genomic strain</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default CropIntelligence;
