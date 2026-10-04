import React from 'react';
import { CircularProgressbarWithChildren, buildStyles } from 'react-circular-progressbar';
import { Wheat, Calendar, Scale, Award } from 'lucide-react';
import StatusBadge from '../ui/StatusBadge';

const HarvestYield = () => {
  const maturityProgress = 85;
  const daysToHarvest = 12;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Wheat className="w-6 h-6 text-agri-gold" />
        <h2 className="text-2xl font-rajdhani font-bold text-gray-200">Harvest & Yield Prediction</h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="glass-card p-8 rounded-2xl border border-agri-gold/30 lg:col-span-1 flex flex-col items-center justify-center relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4">
            <StatusBadge status="active" text="Growing Phase" />
          </div>
          
          <h3 className="text-xl font-rajdhani text-gray-300 mb-8">Crop Maturity</h3>
          
          <div className="w-48 h-48">
            <CircularProgressbarWithChildren 
              value={maturityProgress}
              styles={buildStyles({
                pathColor: '#ffd700',
                trailColor: 'rgba(255, 215, 0, 0.1)',
                strokeLinecap: 'round',
              })}
            >
              <div className="text-center">
                <div className="text-4xl font-space font-bold text-agri-gold glow-text">{maturityProgress}%</div>
                <div className="text-xs text-gray-400 mt-1">Ready</div>
              </div>
            </CircularProgressbarWithChildren>
          </div>

          <div className="mt-8 bg-agri-gold/10 border border-agri-gold/30 px-6 py-3 rounded-full flex items-center gap-3">
            <Calendar className="w-5 h-5 text-agri-gold" />
            <span className="text-gray-200 font-bold">Est. {daysToHarvest} Days to Harvest</span>
          </div>
        </div>

        <div className="lg:col-span-2 space-y-6">
          <div className="glass-card p-6 rounded-xl border border-gray-700">
            <h3 className="text-xl font-rajdhani text-gray-300 mb-6">Yield Forecast</h3>
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-black/30 p-4 rounded-lg border border-gray-700">
                <div className="text-gray-400 text-sm mb-1">Expected Yield</div>
                <div className="text-2xl font-bold text-agri-green">4.2 <span className="text-sm font-normal text-gray-500">Tons/Acre</span></div>
              </div>
              <div className="bg-black/30 p-4 rounded-lg border border-gray-700">
                <div className="text-gray-400 text-sm mb-1">Historical Avg</div>
                <div className="text-2xl font-bold text-gray-300">3.8 <span className="text-sm font-normal text-gray-500">Tons/Acre</span></div>
              </div>
              <div className="bg-black/30 p-4 rounded-lg border border-gray-700">
                <div className="text-gray-400 text-sm mb-1">Variance</div>
                <div className="text-2xl font-bold text-agri-green">+10.5%</div>
              </div>
            </div>

            <div className="mt-8 relative pt-8">
              <div className="absolute top-0 left-0 w-full h-1 bg-gray-800 rounded">
                <div className="absolute top-0 left-0 h-1 bg-gradient-to-r from-agri-green via-agri-gold to-agri-gold rounded w-[85%] relative">
                  <div className="absolute -right-2 -top-2 w-5 h-5 bg-agri-gold rounded-full shadow-[0_0_10px_#ffd700] animate-pulse" />
                </div>
              </div>
              <div className="flex justify-between text-xs text-gray-500 mt-2">
                <span>Seedling</span>
                <span>Vegetative</span>
                <span>Flowering</span>
                <span className="text-agri-gold">Ripening</span>
                <span>Harvest</span>
              </div>
            </div>
          </div>

          <div className="glass-card p-6 rounded-xl border border-gray-700 opacity-60">
            <div className="flex items-center gap-2 mb-4">
              <Scale className="w-5 h-5 text-gray-400" />
              <h3 className="text-xl font-rajdhani text-gray-300">Post-Harvest Entry</h3>
            </div>
            <div className="flex gap-4">
              <input disabled placeholder="Actual Weight (Tons)" className="bg-black/40 border border-gray-700 rounded px-4 py-2 w-full text-gray-500 cursor-not-allowed" />
              <button disabled className="bg-gray-800 text-gray-500 px-6 py-2 rounded cursor-not-allowed">Submit</button>
            </div>
            <p className="text-xs text-gray-500 mt-2">Unlocks when maturity reaches 100%</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HarvestYield;
