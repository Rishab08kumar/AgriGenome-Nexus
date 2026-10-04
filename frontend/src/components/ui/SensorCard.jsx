import React from 'react';
import { motion } from 'framer-motion';
import { Lock } from 'lucide-react';

const SensorCard = ({ title, value, unit, icon: Icon, status = 'normal', disabled = false, chart }) => {
  const getStatusColor = () => {
    switch(status) {
      case 'warning': return 'border-yellow-500 text-yellow-500';
      case 'critical': return 'border-red-500 text-red-500';
      default: return 'border-agri-green text-agri-green';
    }
  };

  const statusColor = getStatusColor();

  if (disabled) {
    return (
      <div className="glass-card relative p-6 rounded-xl border-dashed border-gray-600 opacity-60 flex flex-col items-center justify-center min-h-[200px]">
        <Lock className="w-10 h-10 text-gray-400 mb-2" />
        <h3 className="text-lg font-rajdhani text-gray-400">{title}</h3>
        <div className="absolute inset-0 bg-black/40 rounded-xl flex items-center justify-center backdrop-blur-[2px]">
          <span className="text-gray-300 font-medium px-4 py-2 border border-gray-500 rounded bg-black/50 text-sm">
            Sensor Not Connected
          </span>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      whileHover={{ scale: 1.02, rotateX: 2, rotateY: 2, translateZ: 10 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className={`glass-card p-6 rounded-xl relative overflow-hidden group border ${statusColor.split(' ')[0]}`}
      style={{ transformStyle: "preserve-3d" }}
    >
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:animate-shimmer" />
      
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center gap-2">
          {Icon && <Icon className={`w-5 h-5 ${statusColor.split(' ')[1]}`} />}
          <h3 className="text-lg font-rajdhani font-semibold tracking-wide text-gray-300">{title}</h3>
        </div>
        <div className={`w-3 h-3 rounded-full ${statusColor.split(' ')[0].replace('border-', 'bg-')} animate-pulse`} />
      </div>

      <div className="flex items-baseline gap-2 mb-4">
        <span className={`text-4xl font-bold font-space glow-text ${statusColor.split(' ')[1]}`}>
          {value}
        </span>
        <span className="text-gray-400 text-sm">{unit}</span>
      </div>

      <div className="h-16 w-full">
        {chart}
      </div>
    </motion.div>
  );
};

export default SensorCard;
