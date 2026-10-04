import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Settings, Power, Droplets } from 'lucide-react';
import StatusBadge from '../ui/StatusBadge';

const FieldControl = () => {
  const [pumpActive, setPumpActive] = useState(true);
  const [valveOpen, setValveOpen] = useState(false);

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Settings className="w-6 h-6 text-agri-blue" />
        <h2 className="text-2xl font-rajdhani font-bold text-gray-200">Autonomous Field Control</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className={`glass-card p-6 rounded-xl border flex flex-col items-center justify-center gap-4 transition-all duration-300 ${pumpActive ? 'border-agri-green shadow-[0_0_15px_rgba(0,255,136,0.2)]' : 'border-gray-700'}`}>
          <div className="text-lg text-gray-300">Main Irrigation Pump</div>
          <motion.div 
            animate={{ rotate: pumpActive ? 360 : 0 }} 
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className={`p-4 rounded-full ${pumpActive ? 'bg-agri-green/20 text-agri-green' : 'bg-gray-800 text-gray-500'}`}
          >
            <Power className="w-12 h-12" />
          </motion.div>
          <button 
            onClick={() => setPumpActive(!pumpActive)}
            className={`px-6 py-2 rounded-full font-bold uppercase tracking-wide transition-colors ${pumpActive ? 'bg-agri-green text-black' : 'bg-gray-700 text-white'}`}
          >
            {pumpActive ? 'ON' : 'OFF'}
          </button>
        </div>

        <div className={`glass-card p-6 rounded-xl border flex flex-col items-center justify-center gap-4 transition-all duration-300 ${valveOpen ? 'border-agri-blue shadow-[0_0_15px_rgba(0,180,255,0.2)]' : 'border-gray-700'}`}>
          <div className="text-lg text-gray-300">Nutrient Valve A</div>
          <div className={`p-4 rounded-full transition-colors ${valveOpen ? 'bg-agri-blue/20 text-agri-blue' : 'bg-gray-800 text-gray-500'}`}>
            <Droplets className={`w-12 h-12 ${valveOpen ? 'animate-bounce' : ''}`} />
          </div>
          <button 
            onClick={() => setValveOpen(!valveOpen)}
            className={`px-6 py-2 rounded-full font-bold uppercase tracking-wide transition-colors ${valveOpen ? 'bg-agri-blue text-black' : 'bg-gray-700 text-white'}`}
          >
            {valveOpen ? 'OPEN' : 'CLOSED'}
          </button>
        </div>

        <div className="glass-card p-6 rounded-xl border border-gray-700 flex flex-col justify-center">
          <h3 className="text-lg text-gray-300 mb-4">System Status</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Network</span>
              <StatusBadge status="active" text="Online" />
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Last Dosing</span>
              <span className="text-gray-200">2h ago (N-P-K)</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Next Cycle</span>
              <span className="text-agri-gold font-bold">In 45 mins</span>
            </div>
          </div>
        </div>
      </div>

      <div className="glass-card p-6 rounded-xl border border-gray-700 min-h-[300px] flex items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCI+CjxwYXRoIGQ9Ik0wIDBoNDB2NDBIMHoiIGZpbGw9Im5vbmUiLz4KPHBhdGggZD0iTTAgMTBoNDBWMHoiIGZpbGw9InJnYmEoMCwyNTUsMTM2LDAuMDMpIi8+Cjwvc3ZnPg==')] opacity-50" />
        <div className="text-center relative z-10">
          <div className="w-16 h-16 border-4 border-agri-green border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <h3 className="text-xl font-rajdhani text-agri-green mb-2">3D Farm Map Loading</h3>
          <p className="text-gray-400">Connecting to field sensors...</p>
        </div>
      </div>
    </div>
  );
};

export default FieldControl;
