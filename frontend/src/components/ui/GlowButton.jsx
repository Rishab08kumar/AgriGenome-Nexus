import React from 'react';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';

const GlowButton = ({ children, onClick, loading, className = '', disabled, type = 'button' }) => {
  return (
    <motion.button
      type={type}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      disabled={disabled || loading}
      className={`relative overflow-hidden px-6 py-3 rounded-lg font-medium font-space transition-all duration-300
        bg-gradient-to-r from-agri-green/80 to-agri-blue/80 text-agri-dark
        hover:shadow-[0_0_20px_rgba(0,255,136,0.6)] disabled:opacity-50 disabled:cursor-not-allowed
        ${className}`}
    >
      <div className="absolute inset-0 bg-white/20 -translate-x-full hover:animate-shimmer" />
      <div className="relative flex items-center justify-center gap-2">
        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : children}
      </div>
    </motion.button>
  );
};

export default GlowButton;
