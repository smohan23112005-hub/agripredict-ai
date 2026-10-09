import React, { useState } from 'react';
import { 
  Sprout, 
  Calendar, 
  TrendingUp, 
  CheckCircle2, 
  AlertTriangle, 
  Info,
  ChevronRight,
  ShieldAlert,
  Droplet
} from 'lucide-react';
import { translations } from '../translations';

export default function CropRecommendations({ lang, crops = [], onSelectCrop, selectedCrop }) {
  const t = translations[lang] || translations.en;

  if (!crops || crops.length === 0) {
    return (
      <div className="glass-card rounded-2xl p-8 text-center border border-slate-800">
        <Sprout className="w-12 h-12 text-slate-500 mx-auto mb-3" />
        <p className="text-slate-400 text-sm">No crop recommendations available yet. Run analysis first.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h2 className="text-xl font-bold text-white font-outfit flex items-center space-x-2">
            <span>{t.tabCrops}</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              {crops.length} Best Matches
            </span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Ranked by soil chemistry, water requirements, historical rainfall & seasonal weather suitability
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {crops.map((crop, idx) => {
          const isSelected = (selectedCrop && selectedCrop.crop_name === crop.crop_name) || idx === 0;
          const score = crop.suitability_score || 0;
          const scoreColor = score >= 80 ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30' :
                             score >= 65 ? 'text-teal-400 bg-teal-500/10 border-teal-500/30' :
                             'text-amber-400 bg-amber-500/10 border-amber-500/30';

          return (
            <div
              key={crop.crop_name}
              onClick={() => onSelectCrop && onSelectCrop(crop)}
              className={`glass-card rounded-2xl p-5 border transition-all cursor-pointer relative overflow-hidden ${
                isSelected 
                  ? 'border-emerald-500/50 bg-slate-900/90 shadow-xl shadow-emerald-500/10 ring-1 ring-emerald-500/30' 
                  : 'border-slate-800 hover:border-slate-700 bg-slate-950/60'
              }`}
            >
              {idx === 0 && (
                <div className="absolute top-0 right-0 bg-gradient-to-l from-emerald-500 to-emerald-600 text-slate-950 text-[10px] font-extrabold uppercase px-3 py-1 rounded-bl-xl shadow-md">
                  ★ Top Pick
                </div>
              )}

              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-lg font-bold text-white font-outfit">{crop.crop_name}</span>
                    {crop.crop_name_te && (
                      <span className="text-sm font-medium text-emerald-400">({crop.crop_name_te})</span>
                    )}
                  </div>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold px-2 py-0.5 rounded bg-slate-800/80">
                      {crop.category || 'Agricultural'}
                    </span>
                    <span className="text-[11px] text-slate-400 flex items-center space-x-1">
                      <Droplet className="w-3 h-3 text-sky-400" />
                      <span>{crop.water_requirement || 'Medium'} Water</span>
                    </span>
                  </div>
                </div>

                {/* Score gauge badge */}
                <div className={`px-3 py-1.5 rounded-xl border text-center ${scoreColor}`}>
                  <div className="text-lg font-extrabold font-outfit">{score}%</div>
                  <div className="text-[9px] uppercase tracking-wider font-bold">Match</div>
                </div>
              </div>

              {/* Agronomic Quick Specs */}
              <div className="grid grid-cols-3 gap-2 my-4 pt-3 border-t border-slate-800/80 text-center">
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800/50">
                  <div className="text-[10px] text-slate-400">{t.duration}</div>
                  <div className="text-xs font-semibold text-white mt-0.5">
                    {crop.duration_days || crop.crop_duration_days || 120} days
                  </div>
                </div>
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800/50">
                  <div className="text-[10px] text-slate-400">{t.typicalYield}</div>
                  <div className="text-xs font-semibold text-emerald-400 mt-0.5">
                    {crop.typical_yield_per_acre || 15} Q/acre
                  </div>
                </div>
                <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800/50">
                  <div className="text-[10px] text-slate-400">MSP / Rate</div>
                  <div className="text-xs font-semibold text-white mt-0.5">
                    ₹{crop.typical_price_per_quintal || 2500}/Q
                  </div>
                </div>
              </div>

              {/* Sowing Window Advisory */}
              {crop.recommended_sowing_window && (
                <div className="flex items-center space-x-2 text-xs text-emerald-300 bg-emerald-500/10 px-3 py-2 rounded-xl mb-3 border border-emerald-500/20">
                  <Calendar className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span className="font-medium">{crop.recommended_sowing_window}</span>
                </div>
              )}

              {/* Reasons Why Suitable */}
              {crop.reasons && crop.reasons.length > 0 && (
                <div className="space-y-1.5 pt-2">
                  <div className="text-[11px] font-semibold text-slate-300 flex items-center space-x-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>{t.whySuitable}:</span>
                  </div>
                  <ul className="space-y-1 pl-5 list-disc text-xs text-slate-400">
                    {crop.reasons.slice(0, 3).map((r, i) => (
                      <li key={i} className="leading-tight">{r}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
