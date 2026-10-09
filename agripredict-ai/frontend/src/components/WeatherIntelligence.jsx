import React from 'react';
import { 
  CloudRain, 
  Sun, 
  Wind, 
  Droplets, 
  Thermometer, 
  AlertTriangle, 
  Calendar, 
  TrendingUp,
  ShieldCheck,
  Zap,
  Info
} from 'lucide-react';
import { translations } from '../translations';

export default function WeatherIntelligence({ lang, weather, risk }) {
  const t = translations[lang] || translations.en;

  const current = weather?.current || {};
  const forecast = weather?.forecast?.forecast || [];
  const historical = weather?.historical || {};
  const annualRain = historical?.annual_rainfall || {};
  const heavyRainDays = historical?.heavy_rain_days_per_year || {};
  const risksList = risk?.risks || [];

  const years = Object.keys(annualRain).sort();
  const maxRainfallVal = Math.max(...Object.values(annualRain).map(v => Number(v) || 0), 1000);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white font-outfit flex items-center space-x-2">
          <span>{t.tabWeather}</span>
          <span className="text-xs px-2.5 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20">
            Open-Meteo & IMD Historical Integration
          </span>
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Multi-year climate patterns, real-time agro-meteorology, and field vulnerability assessment
        </p>
      </div>

      {/* Top row: Current weather card + Overall Risk Assessment Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Current Weather Card */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{t.currentWeather}</span>
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Live Station
            </span>
          </div>

          <div className="my-4 flex items-center justify-between">
            <div>
              <div className="text-3xl font-extrabold text-white font-outfit">
                {current.temperature !== undefined ? `${current.temperature}°C` : '--'}
              </div>
              <div className="text-xs text-slate-400 mt-1 capitalize">
                {current.description || 'Partly Cloudy'}
              </div>
            </div>
            <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
              <Sun className="w-6 h-6 animate-pulse" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2 pt-3 border-t border-slate-800 text-xs">
            <div className="flex items-center space-x-2 text-slate-300">
              <Droplets className="w-3.5 h-3.5 text-sky-400" />
              <span>{t.humidity}: {current.humidity !== undefined ? `${current.humidity}%` : '--'}</span>
            </div>
            <div className="flex items-center space-x-2 text-slate-300">
              <Wind className="w-3.5 h-3.5 text-teal-400" />
              <span>Wind: {current.wind_speed !== undefined ? `${current.wind_speed} km/h` : '--'}</span>
            </div>
          </div>
        </div>

        {/* Overall Risk Summary Card */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800 md:col-span-2 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              {lang === 'te' ? 'వాతావరణ ముప్పు విశ్లేషణ' : 'Agro-Climate Risk Index'}
            </span>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
              risk?.overall_risk === 'high' || risk?.overall_risk === 'critical' ? 'bg-red-500/15 text-red-400 border border-red-500/30' :
              risk?.overall_risk === 'moderate' ? 'bg-amber-500/15 text-amber-400 border border-amber-500/30' :
              'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
            }`}>
              {risk?.overall_risk === 'high' ? t.riskHigh :
               risk?.overall_risk === 'moderate' ? t.riskModerate : t.riskLow}
            </span>
          </div>

          <div className="my-3 space-y-2">
            {risksList.length > 0 ? (
              risksList.slice(0, 2).map((item, idx) => (
                <div key={idx} className="flex items-start space-x-3 p-2.5 rounded-xl bg-slate-900/80 border border-slate-800">
                  <AlertTriangle className={`w-4 h-4 mt-0.5 shrink-0 ${
                    item.level === 'high' ? 'text-red-400' :
                    item.level === 'moderate' ? 'text-amber-400' : 'text-emerald-400'
                  }`} />
                  <div className="text-xs">
                    <span className="font-semibold text-slate-200 capitalize">{item.category}: </span>
                    <span className="text-slate-400">{item.description}</span>
                    {item.mitigation && (
                      <div className="text-emerald-400/90 font-medium text-[11px] mt-1">
                        💡 Advisory: {item.mitigation}
                      </div>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <div className="text-xs text-slate-400 py-3 flex items-center space-x-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>No critical climate risks identified for the chosen cropping plan.</span>
              </div>
            )}
          </div>

          <div className="text-[11px] text-slate-400 pt-2 border-t border-slate-800 flex items-center justify-between">
            <span>Historical baseline: 5-Year Weather Distribution</span>
            <span>Forecast Window: 7-Day Observation</span>
          </div>
        </div>
      </div>

      {/* 5-Year Historical Rainfall Interactive Chart Visualizer */}
      <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 className="font-semibold text-white text-base font-outfit flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
              <span>{t.fiveYearTrends}</span>
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Historical precipitation trends and heavy downpour frequency (&ge; 50mm/day)
            </p>
          </div>
          <div className="flex items-center space-x-3 text-xs">
            <span className="flex items-center space-x-1.5 text-slate-300">
              <span className="w-3 h-3 rounded bg-emerald-500 inline-block"></span>
              <span>Total Rainfall (mm)</span>
            </span>
            <span className="flex items-center space-x-1.5 text-slate-300">
              <span className="w-3 h-3 rounded bg-amber-400 inline-block"></span>
              <span>Heavy Rain Days</span>
            </span>
          </div>
        </div>

        {/* Visual Bar Graph */}
        <div className="pt-4 grid grid-cols-5 gap-3 sm:gap-6 items-end min-h-[180px] border-b border-slate-800 pb-3">
          {years.map((year) => {
            const rain = annualRain[year] || 0;
            const heavyDays = heavyRainDays[year] || 0;
            const heightPercent = Math.min(Math.max((rain / maxRainfallVal) * 100, 15), 100);

            return (
              <div key={year} className="flex flex-col items-center space-y-2 group">
                <div className="text-[11px] font-bold text-slate-300 opacity-80 group-hover:opacity-100 transition-opacity">
                  {rain} mm
                </div>
                
                {/* Bar */}
                <div className="w-full max-w-[48px] bg-slate-900 rounded-t-xl overflow-hidden p-1 flex flex-col justify-end h-36 border border-slate-800/80">
                  <div
                    style={{ height: `${heightPercent}%` }}
                    className="w-full bg-gradient-to-t from-emerald-700 to-emerald-400 rounded-t-lg transition-all duration-500 relative group-hover:from-emerald-600 group-hover:to-emerald-300"
                  >
                    {heavyDays > 0 && (
                      <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-amber-400/90 text-slate-950 font-extrabold text-[9px] px-1 rounded-full">
                        {heavyDays}d
                      </span>
                    )}
                  </div>
                </div>

                <div className="text-xs font-semibold text-slate-400 group-hover:text-white transition-colors">
                  {year}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 7-Day Forecast Cards */}
      {forecast.length > 0 && (
        <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-white text-base font-outfit flex items-center space-x-2">
              <Calendar className="w-4 h-4 text-sky-400" />
              <span>{t.forecast7Day}</span>
            </h3>
            <span className="text-xs text-slate-400">Daily Temperature & Precipitation</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-2.5">
            {forecast.map((day, i) => (
              <div
                key={day.date || i}
                className="p-3 rounded-xl bg-slate-900/70 border border-slate-800 text-center flex flex-col justify-between hover:border-slate-700 transition-all"
              >
                <div className="text-[11px] font-semibold text-slate-400">
                  {day.date ? new Date(day.date).toLocaleDateString(undefined, { weekday: 'short', day: 'numeric' }) : `Day ${i+1}`}
                </div>

                <div className="my-2">
                  {day.precipitation > 5 ? (
                    <CloudRain className="w-5 h-5 text-sky-400 mx-auto" />
                  ) : (
                    <Sun className="w-5 h-5 text-amber-400 mx-auto" />
                  )}
                </div>

                <div className="text-xs font-bold text-white">
                  {day.temp_max !== undefined ? `${Math.round(day.temp_max)}°` : '--'}
                  <span className="text-slate-500 font-normal text-[10px] ml-1">
                    {day.temp_min !== undefined ? `${Math.round(day.temp_min)}°` : ''}
                  </span>
                </div>

                <div className="text-[10px] text-sky-400 mt-1 font-medium">
                  {day.precipitation ? `${day.precipitation}mm` : '0mm'}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
