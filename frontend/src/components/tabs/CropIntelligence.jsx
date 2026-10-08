
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Dna,
  Database,
  MapPin,
  Thermometer,
  FlaskConical,
  Activity,
  RefreshCw,
  AlertCircle,
  Sprout,
} from 'lucide-react';

import {
  CircularProgressbar,
  buildStyles,
} from 'react-circular-progressbar';

import 'react-circular-progressbar/dist/styles.css';

import GlowButton from '../ui/GlowButton';

import {
  recommendCrop,
  getLatestSensorData,
} from '../../services/api';

// ======================================
// DEFAULT MANUAL INPUT VALUES
// ======================================

const INITIAL_FORM = {
  latitude: '12.9716',
  longitude: '77.5946',
  soil_moisture: '55',
  temperature: '28',
  humidity: '65',
  light_intensity: '45000',
  nitrogen: '120',
  phosphorus: '45',
  potassium: '80',
  ec: '1.2',
  ph: '',
};

// ======================================
// FLOWER COLORS
// ======================================

const FLOWER_COLORS = {
  Jasmine: '#f5f5f5',
  Rose: '#ff6384',
  Marigold: '#ffbb33',
  Hibiscus: '#ff5555',
  Dianthus: '#ff83b4',
  Chrysanthemum: '#ffd700',
  Carnation: '#ff88aa',
};

const SENSOR_FIELDS = [
  'temperature',
  'humidity',
  'soil_moisture',
  'light_intensity',
  'latitude',
  'longitude',
];

// ======================================
// INPUT FIELD COMPONENT
// ======================================

const InputField = ({
  label,
  name,
  value,
  onChange,
  disabled = false,
  placeholder = '',
}) => (
  <div className="space-y-1">

    <label className="text-xs font-medium uppercase tracking-widest text-gray-400">
      {label}
    </label>

    <input
      type="number"
      step="any"
      name={name}
      value={value}
      onChange={onChange}
      disabled={disabled}
      placeholder={placeholder}
      className={`w-full rounded-lg px-3 py-2.5 text-sm outline-none transition-all border ${
        disabled
          ? 'bg-black/20 border-gray-700 text-gray-400'
          : 'bg-black/40 border-agri-green/30 text-white focus:border-agri-green'
      }`}
    />

  </div>
);

// ======================================
// MAIN COMPONENT
// ======================================

export default function CropIntelligence() {

  const [form, setForm] = useState(INITIAL_FORM);

  const [mode, setMode] = useState('manual');

  const [loading, setLoading] = useState(false);
  const [sensorLoading, setSensorLoading] = useState(false);

  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const [sensorStatus, setSensorStatus] = useState(
    'Manual input mode'
  );

  const [sensorTimestamp, setSensorTimestamp] = useState(null);

  // ======================================
  // FORM INPUT HANDLER
  // ======================================

  const handleChange = (event) => {

    setForm(previous => ({
      ...previous,
      [event.target.name]: event.target.value,
    }));

  };

  // ======================================
  // READ LATEST ESP32 DATA
  // ======================================

  const fetchESP32Data = async () => {

    setSensorLoading(true);
    setError('');

    try {

      const response = await getLatestSensorData();

      const data = response.data;

      if (!data || !data.timestamp) {
        throw new Error(
          'No ESP32 sensor readings available'
        );
      }

      const timestamp = Date.parse(data.timestamp);

      if (
        !Number.isFinite(timestamp) ||
        Date.now() - timestamp > 30000 ||
        timestamp - Date.now() > 5000
      ) {
        throw new Error(
          'ESP32 readings are outdated. Check ESP32 connection.'
        );
      }

      const soil =
        data.soil_percent ??
        data.soil_moisture;

      const light =
        data.lux ??
        data.light_intensity;

      const readings = {
        temperature: data.temperature,
        humidity: data.humidity,
        soil_moisture: soil,
        light_intensity: light,
      };

      for (const [name, value] of Object.entries(readings)) {

        if (
          value === null ||
          value === undefined ||
          value === '' ||
          !Number.isFinite(Number(value))
        ) {
          throw new Error(
            `ESP32 ${name} reading is missing or invalid`
          );
        }
      }

      setForm(previous => ({
        ...previous,

        temperature: String(readings.temperature),
        humidity: String(readings.humidity),
        soil_moisture: String(readings.soil_moisture),
        light_intensity: String(readings.light_intensity),

        latitude: (
          data.latitude !== null &&
          data.latitude !== undefined
        )
          ? String(data.latitude)
          : previous.latitude,

        longitude: (
          data.longitude !== null &&
          data.longitude !== undefined
        )
          ? String(data.longitude)
          : previous.longitude,
      }));

      setSensorTimestamp(timestamp);

      setSensorStatus(
        `ESP32 readings loaded at ${new Date(timestamp).toLocaleTimeString()}`
      );

    } catch (err) {

      setSensorTimestamp(null);
      setSensorStatus('ESP32 data unavailable');

      setError(
        err.response?.data?.detail ||
        err.message ||
        'Failed to load ESP32 readings'
      );

    } finally {

      setSensorLoading(false);

    }
  };

  // ======================================
  // SELECT MANUAL OR SENSOR MODE
  // ======================================

  const changeMode = (newMode) => {

    setMode(newMode);
    setError('');
    setResult(null);
    setSensorTimestamp(null);

    if (newMode === 'manual') {
      setSensorStatus('Manual input mode');
    } else {
      setSensorStatus('Click refresh to load ESP32 data');
    }
  };

  // ======================================
  // SUBMIT RECOMMENDATION
  // ======================================

  const handleSubmit = async (event) => {

    event.preventDefault();

    setError('');
    setResult(null);

    if (mode === 'sensor') {

      if (
        !sensorTimestamp ||
        Date.now() - sensorTimestamp > 30000
      ) {
        setError(
          'Refresh ESP32 readings before running the recommendation.'
        );
        return;
      }
    }

    const payload = {};

    Object.entries(form).forEach(([key, value]) => {

      if (value === '' || value === null) {
        payload[key] = null;
      } else {

        const numeric = Number(value);

        payload[key] = Number.isFinite(numeric)
          ? numeric
          : null;
      }
    });

    const required = [
      'temperature',
      'humidity',
      'soil_moisture',
      'light_intensity',
      'nitrogen',
      'phosphorus',
      'potassium',
      'ec',
    ];

    const missing = required.filter(
      key => payload[key] === null
    );

    if (missing.length > 0) {

      setError(
        `Please provide: ${missing.join(', ')}`
      );
      return;
    }

    if (
      payload.humidity < 0 ||
      payload.humidity > 100 ||
      payload.soil_moisture < 0 ||
      payload.soil_moisture > 100 ||
      payload.light_intensity < 0 ||
      payload.ec < 0 ||
      payload.nitrogen < 0 ||
      payload.phosphorus < 0 ||
      payload.potassium < 0
    ) {
      setError('One or more values are outside valid ranges.');
      return;
    }

    if (
      payload.ph !== null &&
      (payload.ph < 0 || payload.ph > 14)
    ) {
      setError('Soil pH must be between 0 and 14.');
      return;
    }

    payload.latitude ??= 0;
    payload.longitude ??= 0;

    setLoading(true);

    try {

      const response = await recommendCrop(payload);

      const data = response.data;

      // Your current backend response format:
      // {
      //   best_recommendation: {...},
      //   alternatives: [...],
      //   ph_status: "...",
      //   dataset_source: "..."
      // }

      const best = data?.best_recommendation;

      if (!best || !best.flower_species) {
        throw new Error(
          'Backend returned no flower recommendation'
        );
      }

      const confidence = Number(best.confidence);

      if (!Number.isFinite(confidence)) {
        throw new Error(
          'Backend returned invalid confidence'
        );
      }

      if (confidence < 0 || confidence > 100) {
        throw new Error(
          'Backend confidence must be between 0 and 100'
        );
      }

      const normalizedResult = {
        flower: best.flower_species,
        confidence: confidence,
        genomic_strain: best.genomic_strain || '',
        varieties: Array.isArray(best.recommended_varieties)
          ? best.recommended_varieties
          : [],
        alternatives: Array.isArray(data.alternatives)
          ? data.alternatives
          : [],
        dataset_source: data.dataset_source || '',
        ph_status: data.ph_status || '',
        inputs: payload,
      };

      setResult(normalizedResult);

    } catch (err) {

      console.error('Crop recommendation failed:', err);

      const detail = err.response?.data?.detail;

      setError(
        typeof detail === 'string'
          ? detail
          : err.message ||
            'Unable to generate flower recommendation'
      );

    } finally {

      setLoading(false);

    }
  };

  // ======================================
  // DISPLAY VALUES
  // ======================================

  const flowerColor = result
    ? FLOWER_COLORS[result.flower] || '#00ff88'
    : '#00ff88';

  const confidence = result
    ? result.confidence
    : 0;

  // ======================================
  // UI
  // ======================================

  return (

    <div className="relative min-h-[70vh] flex flex-col md:flex-row gap-8">

      {/* INPUT PANEL */}

      <div className="w-full md:w-1/2 glass-card p-6 md:p-8 rounded-2xl border border-agri-green/20">

        <div className="flex items-center gap-3 mb-6">

          <Database className="w-7 h-7 text-agri-green" />

          <div>

            <h2 className="text-xl font-bold text-white">
              Floriculture Intelligence
            </h2>

            <p className="text-xs text-gray-400">
              Flower species and cultivar recommendation
            </p>

          </div>

        </div>

        {/* INPUT MODE */}

        <div className="mb-6 p-4 rounded-xl bg-black/30 border border-gray-700">

          <p className="text-sm text-white mb-3">
            Data Input Mode
          </p>

          <div className="grid grid-cols-2 gap-3">

            <button
              type="button"
              onClick={() => changeMode('manual')}
              className={`rounded-lg p-3 text-sm border ${
                mode === 'manual'
                  ? 'border-agri-green text-agri-green bg-green-500/10'
                  : 'border-gray-700 text-gray-400'
              }`}
            >
              Manual Entry
            </button>

            <button
              type="button"
              onClick={() => changeMode('sensor')}
              className={`rounded-lg p-3 text-sm border ${
                mode === 'sensor'
                  ? 'border-agri-green text-agri-green bg-green-500/10'
                  : 'border-gray-700 text-gray-400'
              }`}
            >
              ESP32 Sensors
            </button>

          </div>

          {mode === 'sensor' && (

            <button
              type="button"
              onClick={fetchESP32Data}
              disabled={sensorLoading}
              className="mt-4 w-full flex justify-center items-center gap-2 p-2 border border-agri-green/40 rounded-lg text-agri-green text-sm"
            >

              <RefreshCw
                size={16}
                className={sensorLoading ? 'animate-spin' : ''}
              />

              {sensorLoading
                ? 'Reading Sensors...'
                : 'Refresh ESP32 Readings'}

            </button>

          )}

          <p className="text-xs text-gray-400 mt-3 flex items-center gap-2">
            <Activity size={14} />
            {sensorStatus}
          </p>

        </div>

        <form onSubmit={handleSubmit} className="space-y-6">

          {/* GPS */}

          <section>

            <div className="flex items-center gap-2 mb-3">
              <MapPin size={16} className="text-agri-blue" />
              <span className="text-sm text-gray-300">
                Field Location
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3">

              <InputField
                label="Latitude"
                name="latitude"
                value={form.latitude}
                onChange={handleChange}
                disabled={mode === 'sensor'}
              />

              <InputField
                label="Longitude"
                name="longitude"
                value={form.longitude}
                onChange={handleChange}
                disabled={mode === 'sensor'}
              />

            </div>

          </section>

          {/* CLIMATE */}

          <section>

            <div className="flex items-center gap-2 mb-3">
              <Thermometer size={16} className="text-yellow-400" />
              <span className="text-sm text-gray-300">
                Climate and Moisture
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3">

              <InputField
                label="Soil Moisture (%)"
                name="soil_moisture"
                value={form.soil_moisture}
                onChange={handleChange}
                disabled={mode === 'sensor'}
              />

              <InputField
                label="Temperature (°C)"
                name="temperature"
                value={form.temperature}
                onChange={handleChange}
                disabled={mode === 'sensor'}
              />

              <InputField
                label="Humidity (%)"
                name="humidity"
                value={form.humidity}
                onChange={handleChange}
                disabled={mode === 'sensor'}
              />

              <InputField
                label="Light (lux)"
                name="light_intensity"
                value={form.light_intensity}
                onChange={handleChange}
                disabled={mode === 'sensor'}
              />

            </div>

          </section>

          {/* MANUAL SOIL INPUTS */}

          <section>

            <div className="flex items-center gap-2 mb-3">
              <FlaskConical size={16} className="text-agri-green" />
              <span className="text-sm text-gray-300">
                Manual Soil Chemistry
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3">

              <InputField
                label="Nitrogen N (mg/kg)"
                name="nitrogen"
                value={form.nitrogen}
                onChange={handleChange}
              />

              <InputField
                label="Phosphorus P (mg/kg)"
                name="phosphorus"
                value={form.phosphorus}
                onChange={handleChange}
              />

              <InputField
                label="Potassium K (mg/kg)"
                name="potassium"
                value={form.potassium}
                onChange={handleChange}
              />

              <InputField
                label="EC (mS/cm)"
                name="ec"
                value={form.ec}
                onChange={handleChange}
              />

              <InputField
                label="Soil pH (optional)"
                name="ph"
                value={form.ph}
                onChange={handleChange}
                placeholder="Enter manually"
              />

            </div>

            <p className="text-xs text-gray-500 mt-2">
              NPK, EC and pH are manually entered.
              No NPK, EC or pH sensor is required.
            </p>

          </section>

          {/* ERROR */}

          {error && (

            <div className="flex gap-2 p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-300 text-sm">

              <AlertCircle size={18} />

              <span>{error}</span>

            </div>

          )}

          <GlowButton
            type="submit"
            loading={loading}
            className="w-full"
          >
            Recommend Flower Variety
          </GlowButton>

        </form>

      </div>

      {/* RESULT PANEL */}

      <div className="w-full md:w-1/2 flex items-center justify-center">

        <AnimatePresence mode="wait">

          {result ? (

            <motion.div
              key="result"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              className="glass-card rounded-2xl p-6 md:p-8 w-full max-w-md text-center border"
              style={{ borderColor: flowerColor }}
            >

              <Dna
                className="w-12 h-12 mx-auto mb-4 text-agri-green"
              />

              <p className="text-xs uppercase tracking-widest text-gray-400 mb-2">
                Recommended Flower
              </p>

              <h2
                className="text-3xl font-bold mb-2"
                style={{ color: flowerColor }}
              >
                {result.flower}
              </h2>

              <p className="text-xs text-gray-400 mb-6">
                {result.genomic_strain}
              </p>

              {/* CONFIDENCE */}

              <div className="w-40 h-40 mx-auto mb-4">

                <CircularProgressbar
                  value={confidence}
                  text={`${confidence.toFixed(1)}%`}
                  styles={buildStyles({
                    pathColor: '#00ff88',
                    textColor: '#00ff88',
                    trailColor: '#203028',
                    textSize: '18px',
                  })}
                />

              </div>

              <p className="text-sm text-gray-400 mb-6">
                Model Confidence
              </p>

              {/* CULTIVARS */}

              <div className="text-left bg-black/30 rounded-xl p-4 mb-5">

                <h3 className="text-agri-green font-bold mb-3">
                  Recommended Cultivars
                </h3>

                {result.varieties.length > 0 ? (

                  result.varieties.map((variety, index) => (

                    <p
                      key={index}
                      className="text-sm text-gray-300 mb-2"
                    >
                      {index + 1}. {variety}
                    </p>

                  ))

                ) : (

                  <p className="text-sm text-gray-500">
                    No individual varieties returned
                  </p>

                )}

              </div>

              {/* ALTERNATIVES */}

              {result.alternatives.length > 0 && (

                <div className="text-left bg-black/30 rounded-xl p-4 mb-5">

                  <h3 className="text-agri-green font-bold mb-3">
                    Alternative Flowers
                  </h3>

                  {result.alternatives.map((item, index) => {

                    const score = Number(item.confidence);

                    return (

                      <div
                        key={index}
                        className="flex justify-between items-center py-2 border-b border-gray-800 last:border-0"
                      >

                        <span className="text-sm text-gray-300">
                          {item.flower_species}
                        </span>

                        <span className="text-sm text-agri-green">
                          {Number.isFinite(score)
                            ? `${score.toFixed(1)}%`
                            : '--'}
                        </span>

                      </div>

                    );

                  })}

                </div>

              )}

              {/* NPK VALUES */}

              <div className="grid grid-cols-3 gap-2 text-xs text-gray-400 mb-5">

                <div className="bg-black/30 rounded-lg p-2">
                  <div className="text-agri-green font-bold">
                    N:{result.inputs.nitrogen}
                  </div>
                  <div>mg/kg</div>
                </div>

                <div className="bg-black/30 rounded-lg p-2">
                  <div className="text-agri-blue font-bold">
                    P:{result.inputs.phosphorus}
                  </div>
                  <div>mg/kg</div>
                </div>

                <div className="bg-black/30 rounded-lg p-2">
                  <div className="text-yellow-400 font-bold">
                    K:{result.inputs.potassium}
                  </div>
                  <div>mg/kg</div>
                </div>

              </div>

              {result.ph_status && (

                <p className="text-xs text-gray-500 mb-2">
                  pH status: {result.ph_status}
                </p>

              )}

              {result.dataset_source && (

                <p className="text-xs text-gray-500 mb-2">
                  Dataset label: {result.dataset_source}
                </p>

              )}

              <p className="text-xs text-gray-500">
                Prototype model recommendation.
                Confirm cultivar suitability using
                local agronomic guidance.
              </p>

            </motion.div>

          ) : (

            <motion.div
              key="empty"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center text-gray-500"
            >

              <Sprout
                className="w-20 h-20 mx-auto mb-4 opacity-40"
              />

              <h3 className="text-xl font-bold mb-2">
                Floriculture AI
              </h3>

              <p className="text-sm">
                Enter field conditions to generate
                a flower recommendation.
              </p>

            </motion.div>

          )}

        </AnimatePresence>

      </div>

    </div>
  );
}
