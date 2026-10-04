import React from 'react';
import { Droplets, Thermometer, Wind, Sun, FlaskConical, Zap, Activity } from 'lucide-react';
import { LineChart, Line, ResponsiveContainer, YAxis } from 'recharts';
import SensorCard from '../ui/SensorCard';
import useFirebase from '../../hooks/useFirebase';

const mockChartData = Array.from({ length: 20 }).map((_, i) => ({ value: 40 + Math.random() * 20 }));

const LiveTelemetry = () => {
  const { sensorData, loading } = useFirebase();

  const getStatus = (val, thresholds) => {
    if (val < thresholds[0] || val > thresholds[3]) return 'critical';
    if (val < thresholds[1] || val > thresholds[2]) return 'warning';
    return 'normal';
  };

  const Chart = ({ color }) => (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={mockChartData}>
        <YAxis domain={['auto', 'auto']} hide />
        <Line 
          type="monotone" 
          dataKey="value" 
          stroke={color} 
          strokeWidth={2} 
          dot={false}
          style={{ filter: `drop-shadow(0px 0px 4px ${color})` }}
        />
      </LineChart>
    </ResponsiveContainer>
  );

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-rajdhani font-bold text-gray-200">Live Telemetry</h2>
        <div className="flex items-center gap-2 text-red-500 bg-red-500/10 px-3 py-1 rounded-full border border-red-500/30">
          <Activity className="w-4 h-4 animate-pulse" />
          <span className="text-sm font-bold tracking-widest uppercase">LIVE</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        <SensorCard 
          title="Soil Moisture" 
          value={sensorData?.moisture || "45"} 
          unit="%" 
          icon={Droplets} 
          status={getStatus(sensorData?.moisture || 45, [20, 30, 60, 80])}
          chart={<Chart color="#00ff88" />}
        />
        <SensorCard 
          title="Temperature" 
          value={sensorData?.temperature || "28"} 
          unit="°C" 
          icon={Thermometer} 
          status={getStatus(sensorData?.temperature || 28, [10, 15, 30, 35])}
          chart={<Chart color="#ffd700" />}
        />
        <SensorCard 
          title="Humidity" 
          value={sensorData?.humidity || "62"} 
          unit="%" 
          icon={Wind} 
          status={getStatus(sensorData?.humidity || 62, [30, 40, 70, 85])}
          chart={<Chart color="#00b4ff" />}
        />
        <SensorCard 
          title="Light Intensity" 
          value={sensorData?.light || "850"} 
          unit="Lux" 
          icon={Sun} 
          status={getStatus(sensorData?.light || 850, [200, 400, 1000, 1200])}
          chart={<Chart color="#ffd700" />}
        />
        <SensorCard 
          title="Nitrogen (N)" 
          value={sensorData?.nitrogen || "120"} 
          unit="mg/kg" 
          icon={FlaskConical} 
          status={getStatus(sensorData?.nitrogen || 120, [50, 80, 150, 200])}
          chart={<Chart color="#00ff88" />}
        />
        <SensorCard 
          title="Phosphorus (P)" 
          value={sensorData?.phosphorus || "45"} 
          unit="mg/kg" 
          icon={FlaskConical} 
          status={getStatus(sensorData?.phosphorus || 45, [20, 30, 60, 80])}
          chart={<Chart color="#00ff88" />}
        />
        <SensorCard 
          title="Electrical Conductivity" 
          value={sensorData?.ec || "1.2"} 
          unit="mS/cm" 
          icon={Zap} 
          status={getStatus(sensorData?.ec || 1.2, [0.5, 0.8, 1.5, 2.0])}
          chart={<Chart color="#00b4ff" />}
        />
        <SensorCard 
          title="Soil pH" 
          value="--" 
          unit="pH" 
          icon={FlaskConical}
          disabled={true}
        />
      </div>
    </div>
  );
};

export default LiveTelemetry;
