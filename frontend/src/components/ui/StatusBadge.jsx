import React from 'react';

const StatusBadge = ({ status, text }) => {
  const getStyles = () => {
    switch (status) {
      case 'active':
      case 'healthy':
      case 'success':
        return 'bg-agri-green/20 text-agri-green border-agri-green shadow-[0_0_10px_rgba(0,255,136,0.3)]';
      case 'warning':
      case 'anomaly':
      case 'deficiency':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.3)]';
      case 'critical':
      case 'pest':
      case 'error':
        return 'bg-red-500/20 text-red-400 border-red-500 shadow-[0_0_10px_rgba(239,68,68,0.3)]';
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500';
    }
  };

  return (
    <div className={`px-3 py-1 rounded-full border text-xs font-semibold uppercase tracking-wider flex items-center gap-2 w-fit ${getStyles()}`}>
      <span className={`w-2 h-2 rounded-full ${status === 'active' ? 'animate-pulse bg-agri-green' : status === 'warning' ? 'bg-yellow-500' : 'bg-red-500'}`} />
      {text}
    </div>
  );
};

export default StatusBadge;
