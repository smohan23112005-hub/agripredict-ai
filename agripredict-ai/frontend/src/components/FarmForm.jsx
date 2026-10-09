import React, { useState } from 'react';
import { 
  MapPin, 
  Layers, 
  Droplets, 
  Calendar, 
  Sparkles, 
  IndianRupee, 
  History, 
  ChevronRight,
  HelpCircle,
  CheckCircle2
} from 'lucide-react';
import { translations } from '../translations';

const AP_DISTRICTS = [
  "Anantapur", "Chittoor", "East Godavari", "Guntur", "Krishna", 
  "Kurnool", "Nellore", "Prakasam", "Srikakulam", "Visakhapatnam", 
  "Vizianagaram", "West Godavari", "YSR Kadapa"
];

const SOIL_TYPES = [
  { value: "red", label: "Red Soil (ఎర్ర నేల)", desc: "Well drained, best for Groundnut, Pulses" },
  { value: "black", label: "Black Soil / Regur (నల్ల రేగడి)", desc: "Moisture retentive, ideal for Cotton, Chilli" },
  { value: "alluvial", label: "Alluvial Soil (ఒండ్రు నేల)", desc: "Highly fertile delta soil, ideal for Paddy, Sugarcane" },
  { value: "loamy", label: "Loamy Soil (మట్టి నేల)", desc: "Balanced texture, suitable for Maize, Vegetables" },
  { value: "sandy", label: "Sandy / Coastal (ఇసుక నేల)", desc: "Rapid drainage, good for Cashew, Groundnut" },
  { value: "clayey", label: "Clayey Soil (బంకమట్టి)", desc: "Heavy water retention, suitable for wetland Paddy" }
];

const IRRIGATION_TYPES = [
  { value: "borewell", label: "Borewell / Tube Well (బోరు బావి)" },
  { value: "canal", label: "Canal Water (కాలువ నీరు)" },
  { value: "tank", label: "Tank / Pond (చెరువు)" },
  { value: "rainfed", label: "Rainfed Only (వర్షాధారం)" },
  { value: "drip", label: "Drip / Micro-Irrigation (బిందు సేద్యం)" }
];

const SEASONS = [
  { value: "kharif", label: "Kharif (Monsoon / ఖరీఫ్)", months: "Jun – Oct" },
  { value: "rabi", label: "Rabi (Winter / రబీ)", months: "Nov – Mar" },
  { value: "zaid", label: "Zaid (Summer / జైద్)", months: "Mar – May" }
];

export default function FarmForm({ lang, onSubmit, loading, onLoadSample }) {
  const t = translations[lang] || translations.en;

  const [formData, setFormData] = useState({
    farmer_name: "Ramesh Babu",
    state: "Andhra Pradesh",
    district: "Chittoor",
    mandal: "Chittoor",
    village: "",
    land_area: 2.5,
    land_unit: "acres",
    soil_type: "red",
    irrigation_type: "borewell",
    farming_season: "kharif",
    previous_crop: "Groundnut",
    budget: 65000,
    planned_sowing_date: "2026-06-15",
    preferred_language: lang,
  });

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ ...formData, preferred_language: lang });
  };

  const handleSampleClick = async () => {
    const sample = await onLoadSample();
    if (sample) {
      setFormData(prev => ({ ...prev, ...sample }));
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header card */}
      <div className="glass-card rounded-2xl p-6 sm:p-8 mb-6 border border-emerald-500/20 relative overflow-hidden shadow-2xl">
        <div className="absolute top-0 right-0 -mt-8 -mr-8 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative z-10">
          <div>
            <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mb-3">
              <Sparkles className="w-3.5 h-3.5" />
              <span>{t.heroBadge}</span>
            </span>
            <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight font-outfit">
              {t.farmPlanningTitle}
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              {t.tagline}
            </p>
          </div>

          <button
            type="button"
            onClick={handleSampleClick}
            className="self-start sm:self-center px-4 py-2.5 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/30 text-xs font-semibold flex items-center space-x-2 transition-all shadow-sm hover:border-emerald-400/50"
          >
            <span>{t.demoDataBtn}</span>
          </button>
        </div>
      </div>

      {/* Main Input Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Step 1: Location & Land */}
        <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-5">
          <div className="flex items-center space-x-2.5 pb-3 border-b border-slate-800/80">
            <MapPin className="w-5 h-5 text-emerald-400" />
            <h3 className="font-semibold text-white text-base">
              {lang === 'te' ? '1. ప్రాంతం మరియు భూమి వివరాలు' : '1. Location & Land Details'}
            </h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {/* Farmer Name */}
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">{t.farmerName}</label>
              <input
                type="text"
                value={formData.farmer_name}
                onChange={(e) => handleChange('farmer_name', e.target.value)}
                placeholder="e.g. Ramesh Babu"
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700/80 text-white text-sm focus:outline-none focus:border-emerald-500 transition-colors"
              />
            </div>

            {/* District */}
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">
                {t.district} <span className="text-emerald-400">*</span>
              </label>
              <select
                value={formData.district}
                onChange={(e) => handleChange('district', e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700/80 text-white text-sm focus:outline-none focus:border-emerald-500 transition-colors"
                required
              >
                {AP_DISTRICTS.map((d) => (
                  <option key={d} value={d} className="bg-slate-900 text-white">
                    {d}
                  </option>
                ))}
              </select>
            </div>

            {/* Mandal */}
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">{t.mandal}</label>
              <input
                type="text"
                value={formData.mandal}
                onChange={(e) => handleChange('mandal', e.target.value)}
                placeholder="e.g. Tirupati / Madanapalle"
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700/80 text-white text-sm focus:outline-none focus:border-emerald-500 transition-colors"
              />
            </div>

            {/* Land Area */}
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">
                {t.landArea} <span className="text-emerald-400">*</span>
              </label>
              <div className="flex space-x-2">
                <input
                  type="number"
                  step="0.5"
                  min="0.1"
                  max="100"
                  value={formData.land_area}
                  onChange={(e) => handleChange('land_area', parseFloat(e.target.value) || 1)}
                  className="w-2/3 px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700/80 text-white text-sm focus:outline-none focus:border-emerald-500 transition-colors"
                  required
                />
                <select
                  value={formData.land_unit}
                  onChange={(e) => handleChange('land_unit', e.target.value)}
                  className="w-1/3 px-2 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700/80 text-white text-xs focus:outline-none focus:border-emerald-500"
                >
                  <option value="acres">{t.acres}</option>
                  <option value="hectares">{t.hectares}</option>
                </select>
              </div>
            </div>

            {/* Planned Sowing Date */}
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">{t.plannedSowingDate}</label>
              <input
                type="date"
                value={formData.planned_sowing_date}
                onChange={(e) => handleChange('planned_sowing_date', e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700/80 text-white text-sm focus:outline-none focus:border-emerald-500 transition-colors"
              />
            </div>

            {/* Budget */}
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">{t.budget}</label>
              <div className="relative">
                <IndianRupee className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="number"
                  step="5000"
                  min="0"
                  value={formData.budget}
                  onChange={(e) => handleChange('budget', parseFloat(e.target.value) || 0)}
                  placeholder="65000"
                  className="w-full pl-9 pr-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700/80 text-white text-sm focus:outline-none focus:border-emerald-500 transition-colors"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Step 2: Soil & Agronomy */}
        <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-5">
          <div className="flex items-center space-x-2.5 pb-3 border-b border-slate-800/80">
            <Layers className="w-5 h-5 text-amber-400" />
            <h3 className="font-semibold text-white text-base">
              {lang === 'te' ? '2. నేల, నీటి వసతి మరియు సాగు కాలం' : '2. Soil, Water & Crop Parameters'}
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Soil Type */}
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-2">{t.soilType}</label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {SOIL_TYPES.map((soil) => (
                  <button
                    key={soil.value}
                    type="button"
                    onClick={() => handleChange('soil_type', soil.value)}
                    className={`p-3 rounded-xl text-left border transition-all ${
                      formData.soil_type === soil.value
                        ? 'bg-emerald-500/15 border-emerald-500/60 text-white ring-1 ring-emerald-500/30'
                        : 'bg-slate-900/70 border-slate-800 text-slate-300 hover:border-slate-700'
                    }`}
                  >
                    <div className="text-xs font-semibold flex items-center justify-between">
                      <span>{soil.label}</span>
                      {formData.soil_type === soil.value && (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                      )}
                    </div>
                    <div className="text-[11px] text-slate-400 mt-1 leading-tight">{soil.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Irrigation & Season */}
            <div className="space-y-4">
              {/* Irrigation */}
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">{t.irrigationType}</label>
                <select
                  value={formData.irrigation_type}
                  onChange={(e) => handleChange('irrigation_type', e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700/80 text-white text-sm focus:outline-none focus:border-emerald-500"
                >
                  {IRRIGATION_TYPES.map((irr) => (
                    <option key={irr.value} value={irr.value} className="bg-slate-900">
                      {irr.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Season */}
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">{t.season}</label>
                <div className="grid grid-cols-3 gap-2">
                  {SEASONS.map((s) => (
                    <button
                      key={s.value}
                      type="button"
                      onClick={() => handleChange('farming_season', s.value)}
                      className={`p-2.5 rounded-xl text-center border transition-all ${
                        formData.farming_season === s.value
                          ? 'bg-emerald-500/15 border-emerald-500/60 text-white'
                          : 'bg-slate-900/70 border-slate-800 text-slate-300 hover:border-slate-700'
                      }`}
                    >
                      <div className="text-xs font-semibold">{s.label.split(' ')[0]}</div>
                      <div className="text-[10px] text-slate-400">{s.months}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Previous Crop */}
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">{t.previousCrop}</label>
                <input
                  type="text"
                  value={formData.previous_crop}
                  onChange={(e) => handleChange('previous_crop', e.target.value)}
                  placeholder="e.g. Groundnut, Cotton, Rice, None"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700/80 text-white text-sm focus:outline-none focus:border-emerald-500 transition-colors"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Submit Action */}
        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={loading}
            className={`w-full sm:w-auto px-8 py-4 rounded-xl font-semibold text-sm flex items-center justify-center space-x-3 transition-all shadow-xl ${
              loading
                ? 'bg-emerald-700/50 text-emerald-200 cursor-not-allowed'
                : 'bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-slate-950 font-bold hover:shadow-emerald-500/25 active:scale-[0.99]'
            }`}
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                <span>{t.analyzing}</span>
              </>
            ) : (
              <>
                <span>{t.analyzeBtn}</span>
                <ChevronRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
