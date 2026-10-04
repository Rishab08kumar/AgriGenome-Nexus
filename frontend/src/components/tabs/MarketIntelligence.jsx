import React from 'react';
import { TrendingUp, TrendingDown, IndianRupee, MapPin } from 'lucide-react';
import { ComposedChart, Line, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Jan', actual: 2100, forecast: null },
  { name: 'Feb', actual: 2150, forecast: null },
  { name: 'Mar', actual: 2200, forecast: null },
  { name: 'Apr', actual: 2180, forecast: null },
  { name: 'May', actual: 2250, forecast: 2250 },
  { name: 'Jun', actual: null, forecast: 2300, min: 2200, max: 2400 },
  { name: 'Jul', actual: null, forecast: 2350, min: 2250, max: 2500 },
  { name: 'Aug', actual: null, forecast: 2400, min: 2300, max: 2600 },
];

const MarketIntelligence = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <TrendingUp className="w-6 h-6 text-agri-blue" />
          <h2 className="text-2xl font-rajdhani font-bold text-gray-200">Market Intelligence</h2>
        </div>
        <div className="flex gap-2">
          <select className="bg-black/50 border border-gray-700 rounded px-3 py-1 text-sm text-gray-300">
            <option>Wheat (Grade A)</option>
            <option>Rice (Basmati)</option>
          </select>
          <select className="bg-black/50 border border-gray-700 rounded px-3 py-1 text-sm text-gray-300">
            <option>Delhi APMC</option>
            <option>Punjab APMC</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <div className="glass-card p-6 rounded-xl border border-agri-blue/30 relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-br from-agri-blue/10 to-transparent" />
            <h3 className="text-gray-400 text-sm mb-2 relative z-10">Current Spot Price</h3>
            <div className="flex items-baseline gap-1 relative z-10">
              <IndianRupee className="w-6 h-6 text-agri-blue" />
              <span className="text-4xl font-bold text-white">2,250</span>
              <span className="text-sm text-gray-400">/ Quintal</span>
            </div>
            <div className="mt-4 flex items-center gap-2 text-agri-green text-sm relative z-10 bg-agri-green/10 w-fit px-2 py-1 rounded">
              <TrendingUp className="w-4 h-4" />
              <span>+2.4% vs last week</span>
            </div>
          </div>

          <div className="glass-card p-6 rounded-xl border border-gray-700">
            <h3 className="text-gray-400 text-sm mb-4">Market Sentiment</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-300">Demand</span>
                  <span className="text-agri-green">High</span>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-1.5">
                  <div className="bg-agri-green h-1.5 rounded-full" style={{ width: '85%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-300">Supply</span>
                  <span className="text-yellow-500">Moderate</span>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-1.5">
                  <div className="bg-yellow-500 h-1.5 rounded-full" style={{ width: '45%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-3 glass-card p-6 rounded-xl border border-gray-700">
          <h3 className="text-xl font-rajdhani text-gray-300 mb-6">6-Month Price Forecast</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00b4ff" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#00b4ff" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="name" stroke="#666" tick={{ fill: '#999' }} />
                <YAxis domain={['dataMin - 100', 'dataMax + 100']} stroke="#666" tick={{ fill: '#999' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'rgba(10, 15, 10, 0.9)', borderColor: '#333', borderRadius: '8px' }}
                  itemStyle={{ color: '#e0ffe0' }}
                />
                
                {/* Historical Data */}
                <Line type="monotone" dataKey="actual" stroke="#00ff88" strokeWidth={3} dot={{ r: 4, fill: '#0a0f0a', stroke: '#00ff88' }} />
                
                {/* Forecast Area (Min-Max) */}
                <Area type="monotone" dataKey="max" stroke="none" fill="url(#colorForecast)" />
                
                {/* Forecast Line */}
                <Line type="monotone" dataKey="forecast" stroke="#00b4ff" strokeWidth={2} strokeDasharray="5 5" dot={{ r: 4, fill: '#0a0f0a', stroke: '#00b4ff' }} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketIntelligence;
