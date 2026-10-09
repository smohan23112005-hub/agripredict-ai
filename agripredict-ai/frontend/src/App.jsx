import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import FarmForm from './components/FarmForm';
import CropRecommendations from './components/CropRecommendations';
import WeatherIntelligence from './components/WeatherIntelligence';
import FinancialEstimator from './components/FinancialEstimator';
import ReportModal from './components/ReportModal';
import { api } from './services/api';
import { translations } from './translations';
import { 
  Sprout, 
  CloudSun, 
  IndianRupee, 
  FileText, 
  RotateCcw, 
  CheckCircle2, 
  AlertCircle,
  Sparkles,
  ArrowRight
} from 'lucide-react';

export default function App() {
  const [lang, setLang] = useState('en');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState('checking');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [selectedCrop, setSelectedCrop] = useState(null);
  const [activeTab, setActiveTab] = useState('crops'); // 'crops' | 'weather' | 'finance' | 'reports'

  const t = translations[lang] || translations.en;

  // Check health on mount
  useEffect(() => {
    async function check() {
      const res = await api.checkHealth();
      setBackendStatus(res.status === 'healthy' || res.status === 'ok' ? 'online' : 'demo');
    }
    check();
  }, []);

  // Handle Form Submit
  const handleFormSubmit = async (farmInput) => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.analyzeFarm(farmInput);
      setAnalysisResult(result);
      if (result?.crops && result.crops.length > 0) {
        setSelectedCrop(result.crops[0]);
      }
      setActiveTab('crops');
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'Analysis failed. Please check network connection.');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadSample = async () => {
    return await api.getSampleFarm();
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setSelectedCrop(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-emerald-500 selection:text-slate-950">
      {/* Top Navbar */}
      <Navbar lang={lang} setLang={setLang} backendStatus={backendStatus} />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error notification banner */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
            <button onClick={() => setError(null)} className="font-bold underline ml-4">
              Dismiss
            </button>
          </div>
        )}

        {!analysisResult ? (
          /* Initial View: Planning Wizard */
          <FarmForm
            lang={lang}
            onSubmit={handleFormSubmit}
            loading={loading}
            onLoadSample={handleLoadSample}
          />
        ) : (
          /* Results Dashboard View */
          <div className="space-y-6">
            {/* Top Result Banner */}
            <div className="glass-card rounded-2xl p-6 border border-emerald-500/30 bg-gradient-to-r from-emerald-950/40 via-slate-900 to-slate-900 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
                    {t.resultsTitle}
                  </span>
                </div>
                <h1 className="text-2xl font-bold text-white font-outfit mt-1">
                  {analysisResult.farm?.farmer_name || 'Farmer'}’s Farm — {analysisResult.farm?.district}, {analysisResult.farm?.state}
                </h1>
                <p className="text-xs text-slate-400 mt-0.5">
                  {analysisResult.farm?.land_area} {analysisResult.farm?.land_unit} • {analysisResult.farm?.soil_type} Soil • {analysisResult.farm?.farming_season} Season
                </p>
              </div>

              <div className="flex items-center space-x-3">
                <button
                  onClick={handleReset}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold flex items-center space-x-2 border border-slate-700 transition-all"
                >
                  <RotateCcw className="w-3.5 h-3.5 text-emerald-400" />
                  <span>{t.newAnalysis}</span>
                </button>
              </div>
            </div>

            {/* Navigation Tabs */}
            <div className="flex items-center space-x-2 overflow-x-auto pb-2 border-b border-slate-800">
              <button
                onClick={() => setActiveTab('crops')}
                className={`px-4 py-2.5 rounded-xl text-xs font-semibold flex items-center space-x-2 transition-all shrink-0 ${
                  activeTab === 'crops'
                    ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20 font-bold'
                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                <Sprout className="w-4 h-4" />
                <span>{t.tabCrops}</span>
              </button>

              <button
                onClick={() => setActiveTab('weather')}
                className={`px-4 py-2.5 rounded-xl text-xs font-semibold flex items-center space-x-2 transition-all shrink-0 ${
                  activeTab === 'weather'
                    ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20 font-bold'
                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                <CloudSun className="w-4 h-4" />
                <span>{t.tabWeather}</span>
              </button>

              <button
                onClick={() => setActiveTab('finance')}
                className={`px-4 py-2.5 rounded-xl text-xs font-semibold flex items-center space-x-2 transition-all shrink-0 ${
                  activeTab === 'finance'
                    ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20 font-bold'
                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                <IndianRupee className="w-4 h-4" />
                <span>{t.tabFinance}</span>
              </button>

              <button
                onClick={() => setActiveTab('reports')}
                className={`px-4 py-2.5 rounded-xl text-xs font-semibold flex items-center space-x-2 transition-all shrink-0 ${
                  activeTab === 'reports'
                    ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20 font-bold'
                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                <FileText className="w-4 h-4" />
                <span>{t.tabReport}</span>
              </button>
            </div>

            {/* Tab Panes */}
            <div>
              {activeTab === 'crops' && (
                <CropRecommendations
                  lang={lang}
                  crops={analysisResult.crops}
                  selectedCrop={selectedCrop}
                  onSelectCrop={(crop) => {
                    setSelectedCrop(crop);
                  }}
                />
              )}

              {activeTab === 'weather' && (
                <WeatherIntelligence
                  lang={lang}
                  weather={analysisResult.weather}
                  risk={analysisResult.risk}
                />
              )}

              {activeTab === 'finance' && (
                <FinancialEstimator
                  lang={lang}
                  finance={analysisResult.finance}
                  cropName={selectedCrop?.crop_name || analysisResult.crops?.[0]?.crop_name}
                  landArea={analysisResult.farm?.land_area}
                  landUnit={analysisResult.farm?.land_unit}
                />
              )}

              {activeTab === 'reports' && (
                <ReportModal
                  lang={lang}
                  analysisId={analysisResult.analysis_id}
                  farmData={analysisResult.farm}
                  dataSources={analysisResult.data_sources}
                />
              )}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>🌾 AgriPredict AI — College Hackathon MVP</span>
          <span>Open-Meteo & IMD Historicals • Random Forest Agronomy • Bilingual Telugu & English</span>
        </div>
      </footer>
    </div>
  );
}
