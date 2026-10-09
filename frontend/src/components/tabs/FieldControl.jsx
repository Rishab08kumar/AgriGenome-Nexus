import React from 'react';
import { Activity, Droplets, MapPin, Power, Thermometer, WifiOff } from 'lucide-react';
import { useLiveESP32 } from '../../hooks/useLiveESP32';

const panel = 'glass-card rounded-xl border border-agri-green/20 p-5 bg-black/30';
const show = (x, suffix = '') => x === null ? '—' : `${x.toFixed(1)}${suffix}`;

export default function FieldControl() {
  const { reading, fresh, loading, error, ageSeconds, value } = useLiveESP32();
  const moisture = value('soil_percent', reading?.soil_moisture);
  const temperature = value('temperature');
  const humidity = value('humidity');
  const lux = value('lux', reading?.light_intensity);
  const lat = value('latitude');
  const lng = value('longitude');
  const gpsValid = lat !== null && lng !== null && !(lat === 0 && lng === 0);
  const pumpKnown = fresh && typeof reading?.pump_status === 'boolean';
  const pumpOn = pumpKnown && reading.pump_status;
  const pumpLabel = !pumpKnown ? 'UNKNOWN / OFFLINE' : pumpOn ? 'ON' : 'OFF';
  const pumpColor = !pumpKnown ? 'text-yellow-400' : pumpOn ? 'text-agri-green' : 'text-gray-300';

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div><h2 className="text-3xl font-bold text-agri-green">Live Field Control</h2><p className="text-gray-400 text-sm mt-1">Read-only view of ESP32-reported hardware state. Pump automation runs on the ESP32.</p></div>
        <span className={`rounded-lg px-3 py-2 border text-sm ${fresh ? 'border-green-500 text-green-300' : 'border-yellow-600 text-yellow-300'}`}>
          {fresh ? `LIVE · ${ageSeconds}s ago` : loading ? 'CONNECTING' : 'OFFLINE / STALE'}
        </span>
      </div>
      {error && <div role="alert" className="text-yellow-300 bg-yellow-950/30 border border-yellow-600/30 p-3 rounded-lg">{error}</div>}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
        <section className={panel}>
          <div className="flex gap-2 items-center text-gray-400"><Power size={18}/> Pump reported by ESP32</div>
          <p className={`text-3xl font-bold mt-3 ${pumpColor}`}>{pumpLabel}</p>
          <p className="text-xs text-gray-500 mt-2">This is firmware-reported state, not a physical flow measurement.</p>
        </section>
        <section className={panel}><div className="flex items-center gap-2 text-gray-400"><Droplets size={18}/> Soil moisture</div><p className="text-3xl font-bold mt-3">{show(moisture,'%')}</p></section>
        <section className={panel}><div className="flex items-center gap-2 text-gray-400"><Thermometer size={18}/> Temperature</div><p className="text-3xl font-bold mt-3">{temperature !== null && temperature >= -40 && temperature <= 85 ? show(temperature,'°C') : '—'}</p></section>
        <section className={panel}><div className="flex items-center gap-2 text-gray-400"><Activity size={18}/> Humidity</div><p className="text-3xl font-bold mt-3">{humidity !== null && humidity >= 0 && humidity <= 100 ? show(humidity,'%') : '—'}</p></section>
        <section className={panel}><div className="flex items-center gap-2 text-gray-400"><Activity size={18}/> Light</div><p className="text-3xl font-bold mt-3">{show(lux,' lux')}</p></section>
        <section className={panel}><div className="flex items-center gap-2 text-gray-400"><MapPin size={18}/> GPS position</div><p className="text-lg font-bold mt-3">{gpsValid ? `${lat.toFixed(6)}, ${lng.toFixed(6)}` : 'No GPS fix'}</p></section>
      </div>
      <div className={panel}>
        <h3 className="font-semibold text-lg mb-2">Connected data source</h3>
        <p className="text-gray-300 text-sm">Device: {fresh ? reading?.device_id || 'Unspecified' : 'Unavailable'}</p>
        <p className="text-gray-400 text-sm">Timestamp: {reading?.timestamp || 'No reading'}</p>
        <p className="text-yellow-300 text-xs mt-3 flex gap-2"><WifiOff size={16}/> No browser ON/OFF controls: they would only change the screen, not your real relay.</p>
        <p className="text-gray-400 text-xs mt-2">NPK, pH and EC are unavailable unless measured or manually entered. A model must not treat missing values as real sensor data.</p>
      </div>
    </div>
  );
}
