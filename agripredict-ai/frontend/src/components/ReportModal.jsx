import React from 'react';
import { 
  FileText, 
  Download, 
  Table, 
  ExternalLink, 
  CheckCircle2, 
  Info,
  Layers,
  Database
} from 'lucide-react';
import { translations } from '../translations';
import { api } from '../services/api';

export default function ReportModal({ lang, analysisId, farmData, dataSources }) {
  const t = translations[lang] || translations.en;

  const pdfUrl = analysisId ? api.getPdfReportUrl(analysisId, lang) : '#';
  const csvUrl = analysisId ? api.getCsvReportUrl(analysisId) : '#';

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white font-outfit flex items-center space-x-2">
          <span>{t.tabReport}</span>
          <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            Export & Provenance
          </span>
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Download executive advisory documents and inspect data source governance
        </p>
      </div>

      {/* Download Action Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* PDF Card */}
        <div className="glass-card rounded-2xl p-6 border border-slate-800 flex flex-col justify-between hover:border-emerald-500/30 transition-all group">
          <div>
            <div className="w-10 h-10 rounded-xl bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-400 mb-3">
              <FileText className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-white text-base font-outfit">Official Advisory PDF</h3>
            <p className="text-xs text-slate-400 mt-1">
              Formatted multi-page advisory report with crop recommendations, weather hazard index, and financial breakdown.
            </p>
          </div>

          <a
            href={pdfUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-5 w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs flex items-center justify-center space-x-2 transition-all shadow-md group-hover:shadow-emerald-500/20"
          >
            <Download className="w-4 h-4" />
            <span>{t.downloadPdf}</span>
          </a>
        </div>

        {/* CSV Card */}
        <div className="glass-card rounded-2xl p-6 border border-slate-800 flex flex-col justify-between hover:border-teal-500/30 transition-all group">
          <div>
            <div className="w-10 h-10 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-400 mb-3">
              <Table className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-white text-base font-outfit">Raw Analytics CSV</h3>
            <p className="text-xs text-slate-400 mt-1">
              Tabular export with 5-year precipitation data, suitability score matrix, and financial lines.
            </p>
          </div>

          <a
            href={csvUrl}
            download={`agripredict_analysis_${analysisId || 'export'}.csv`}
            className="mt-5 w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs flex items-center justify-center space-x-2 border border-slate-700 transition-all"
          >
            <Download className="w-4 h-4 text-teal-400" />
            <span>{t.downloadCsv}</span>
          </a>
        </div>
      </div>

      {/* Data Sources & Model Governance */}
      <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
        <div className="flex items-center space-x-2">
          <Database className="w-5 h-5 text-indigo-400" />
          <h3 className="font-semibold text-white text-base font-outfit">{t.dataSources}</h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
          <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
            <div className="font-semibold text-slate-200">Weather Observations & Forecasts</div>
            <div className="text-slate-400 mt-1">
              Open-Meteo API (Historical ECMWF ERA5 & GFS Forecast Models). Resolves district coordinates for Andhra Pradesh.
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
            <div className="font-semibold text-slate-200">AI Crop Suitability Model</div>
            <div className="text-slate-400 mt-1">
              Random Forest Classifier trained on AP agricultural soil, rainfall tolerance, and temperature agronomic standards.
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
            <div className="font-semibold text-slate-200">Financial Modeling</div>
            <div className="text-slate-400 mt-1">
              Cost-of-cultivation templates based on AP Agriculture Department & CACP benchmarks adjusted for farm scale.
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
            <div className="font-semibold text-slate-200">Offline & Demo Capabilities</div>
            <div className="text-slate-400 mt-1">
              Full offline fallback ensures uninterrupted presentations with realistic benchmark profiles even without internet.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
