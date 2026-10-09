import React, { useState } from 'react';
import { 
  IndianRupee, 
  TrendingUp, 
  PieChart as PieIcon, 
  ShieldAlert, 
  Sliders, 
  CheckCircle2,
  DollarSign,
  AlertCircle
} from 'lucide-react';
import { translations } from '../translations';

export default function FinancialEstimator({ lang, finance, cropName, landArea = 2, landUnit = 'acres' }) {
  const t = translations[lang] || translations.en;

  const baseCost = finance?.total_cultivation_cost || 50000;
  const baseYield = finance?.estimated_yield || 20;
  const basePrice = finance?.typical_price_per_quintal || (finance?.estimated_gross_revenue ? Math.round(finance.estimated_gross_revenue / (baseYield || 1)) : 2500);

  // Dynamic sensitivity sliders
  const [priceAdjustment, setPriceAdjustment] = useState(0); // percentage (-30% to +30%)
  const [yieldAdjustment, setYieldAdjustment] = useState(0); // percentage (-30% to +30%)

  const currentPrice = Math.round(basePrice * (1 + priceAdjustment / 100));
  const currentYield = Number((baseYield * (1 + yieldAdjustment / 100)).toFixed(1));
  const grossRevenue = Math.round(currentYield * currentPrice);
  const totalCost = Math.round(baseCost);
  const netReturn = grossRevenue - totalCost;
  const roi = totalCost > 0 ? Math.round((netReturn / totalCost) * 100) : 0;
  const breakEvenPrice = currentYield > 0 ? Math.round(totalCost / currentYield) : 0;

  const costBreakdown = finance?.cost_breakdown || {
    "Seeds & Nursery": Math.round(totalCost * 0.15),
    "Fertilizers & Nutrients": Math.round(totalCost * 0.20),
    "Plant Protection / Pesticides": Math.round(totalCost * 0.12),
    "Labor & Machinery": Math.round(totalCost * 0.30),
    "Irrigation & Power": Math.round(totalCost * 0.08),
    "Harvesting & Post-Harvest": Math.round(totalCost * 0.10),
    "Miscellaneous": Math.round(totalCost * 0.05),
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white font-outfit flex items-center space-x-2">
          <span>{t.tabFinance}</span>
          <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            For {cropName || 'Selected Crop'} ({landArea} {landUnit})
          </span>
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Detailed cost of cultivation, yield projection, net profit forecasting, and sensitivity scenarios
        </p>
      </div>

      {/* Top 3 Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Total Cost */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{t.totalCost}</div>
          <div className="text-2xl font-extrabold text-white font-outfit mt-2">
            ₹{totalCost.toLocaleString('en-IN')}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            ₹{Math.round(totalCost / (landArea || 1)).toLocaleString('en-IN')} / {landUnit.slice(0, -1) || 'acre'}
          </div>
        </div>

        {/* Projected Gross Revenue */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{t.grossRevenue}</div>
          <div className="text-2xl font-extrabold text-teal-400 font-outfit mt-2">
            ₹{grossRevenue.toLocaleString('en-IN')}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            Est. Yield: {currentYield} Quintals @ ₹{currentPrice}/Q
          </div>
        </div>

        {/* Estimated Net Return */}
        <div className={`glass-card rounded-2xl p-5 border ${
          netReturn >= 0 ? 'border-emerald-500/30 bg-emerald-950/10' : 'border-red-500/30 bg-red-950/10'
        }`}>
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{t.netReturn}</div>
          <div className={`text-2xl font-extrabold font-outfit mt-2 ${netReturn >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
            ₹{netReturn.toLocaleString('en-IN')}
          </div>
          <div className="text-[11px] text-slate-300 mt-1 font-medium">
            ROI: <span className={roi >= 0 ? 'text-emerald-400 font-bold' : 'text-red-400 font-bold'}>{roi}%</span> | Break-Even: ₹{breakEvenPrice}/Q
          </div>
        </div>
      </div>

      {/* Main Grid: Cost Breakdown & What-if Interactive Calculator */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Cost Breakdown */}
        <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
          <div className="flex items-center space-x-2">
            <PieIcon className="w-5 h-5 text-emerald-400" />
            <h3 className="font-semibold text-white text-base">{t.costBreakdown}</h3>
          </div>

          <div className="space-y-3 pt-2">
            {Object.entries(costBreakdown).map(([category, amount]) => {
              const pct = totalCost > 0 ? Math.round((amount / totalCost) * 100) : 0;
              return (
                <div key={category} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-300 font-medium">{category}</span>
                    <span className="text-white font-semibold">₹{Number(amount).toLocaleString('en-IN')} ({pct}%)</span>
                  </div>
                  <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden">
                    <div
                      className="bg-emerald-500 h-full rounded-full transition-all duration-300"
                      style={{ width: `${pct}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Interactive What-If Scenario Simulator */}
        <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Sliders className="w-5 h-5 text-amber-400" />
              <h3 className="font-semibold text-white text-base">
                {lang === 'te' ? 'ఆదాయ దృశ్య అనుకరణ (What-If)' : 'Market & Yield Sensitivity'}
              </h3>
            </div>
            <button
              onClick={() => { setPriceAdjustment(0); setYieldAdjustment(0); }}
              className="text-[11px] text-slate-400 hover:text-emerald-400 transition-colors"
            >
              Reset
            </button>
          </div>

          <div className="space-y-4 pt-2">
            {/* Price Slider */}
            <div>
              <div className="flex justify-between text-xs text-slate-300 mb-1.5">
                <span>Market Selling Price Variance</span>
                <span className="font-bold text-amber-400">{priceAdjustment >= 0 ? `+${priceAdjustment}%` : `${priceAdjustment}%`} (₹{currentPrice}/Q)</span>
              </div>
              <input
                type="range"
                min="-30"
                max="30"
                step="5"
                value={priceAdjustment}
                onChange={(e) => setPriceAdjustment(Number(e.target.value))}
                className="w-full accent-amber-400 bg-slate-800 rounded-lg cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500 mt-0.5">
                <span>-30% (Distress Sale)</span>
                <span>Baseline (₹{basePrice})</span>
                <span>+30% (High Demand)</span>
              </div>
            </div>

            {/* Yield Slider */}
            <div>
              <div className="flex justify-between text-xs text-slate-300 mb-1.5">
                <span>Crop Yield Variance</span>
                <span className="font-bold text-teal-400">{yieldAdjustment >= 0 ? `+${yieldAdjustment}%` : `${yieldAdjustment}%`} ({currentYield} Q)</span>
              </div>
              <input
                type="range"
                min="-30"
                max="30"
                step="5"
                value={yieldAdjustment}
                onChange={(e) => setYieldAdjustment(Number(e.target.value))}
                className="w-full accent-teal-400 bg-slate-800 rounded-lg cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500 mt-0.5">
                <span>-30% (Weather Impact)</span>
                <span>Standard ({baseYield} Q)</span>
                <span>+30% (Bumper Harvest)</span>
              </div>
            </div>

            {/* Scenario Output Box */}
            <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2 text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Simulated Net Profit:</span>
                <span className={`font-bold text-sm ${netReturn >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                  ₹{netReturn.toLocaleString('en-IN')}
                </span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Safety Buffer / MSP Margin:</span>
                <span className="text-white font-medium">
                  {currentPrice > breakEvenPrice ? `+₹${currentPrice - breakEvenPrice}/Q above break-even` : 'Below break-even threshold'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
