import React from 'react';
import { Sprout, Languages, ShieldCheck, Activity } from 'lucide-react';
import { translations } from '../translations';

export default function Navbar({ lang, setLang, backendStatus }) {
  const t = translations[lang] || translations.en;

  return (
    <header className="sticky top-0 z-50 glass-card border-b border-slate-800/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo & Brand */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-emerald-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <Sprout className="w-6 h-6 text-slate-950 stroke-[2.5]" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-white tracking-tight font-outfit">AgriPredict AI</span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Andhra Pradesh
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              {lang === 'te' ? 'స్మార్ట్ పంట ప్రణాళిక & రిస్క్ ప్రిడిక్షన్' : 'Smart Crop Planning & Risk System'}
            </p>
          </div>
        </div>

        {/* Right side controls: Health status + Language switcher */}
        <div className="flex items-center space-x-3">
          {/* Backend Status */}
          <div className="hidden md:flex items-center space-x-2 px-3 py-1 rounded-full text-xs bg-slate-900 border border-slate-800">
            <span className={`w-2 h-2 rounded-full ${backendStatus === 'online' ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
            <span className="text-slate-300">
              {backendStatus === 'online' ? 'FastAPI Connected' : 'Demo / Standalone'}
            </span>
          </div>

          {/* Language Switcher */}
          <button
            onClick={() => setLang(lang === 'en' ? 'te' : 'en')}
            className="flex items-center space-x-2 px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-medium transition-all shadow-sm"
          >
            <Languages className="w-4 h-4 text-emerald-400" />
            <span>{lang === 'en' ? 'తెలుగు (Telugu)' : 'English'}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
