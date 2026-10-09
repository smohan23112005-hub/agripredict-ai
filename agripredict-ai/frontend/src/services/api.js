const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const api = {
  // Check backend health
  async checkHealth() {
    try {
      const res = await fetch(`${API_BASE_URL}/health`);
      return await res.json();
    } catch (err) {
      console.warn("Backend offline or unreachable, using offline fallback", err);
      return { status: "offline" };
    }
  },

  // Get sample demo farm input
  async getSampleFarm() {
    try {
      const res = await fetch(`${API_BASE_URL}/farm/sample`);
      if (!res.ok) throw new Error("Failed to load sample");
      return await res.json();
    } catch {
      return {
        farmer_name: "Ramesh Babu",
        state: "Andhra Pradesh",
        district: "Chittoor",
        mandal: "Chittoor",
        land_area: 2.5,
        land_unit: "acres",
        soil_type: "red",
        irrigation_type: "borewell",
        farming_season: "kharif",
        previous_crop: "Groundnut",
        preferred_crops: [],
        planned_sowing_date: "2026-06-15",
        budget: 65000,
        preferred_language: "en",
      };
    }
  },

  // Analyze Farm
  async analyzeFarm(farmData) {
    const res = await fetch(`${API_BASE_URL}/farm/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(farmData),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: 'Failed to analyze farm' }));
      throw new Error(errorData.detail || 'Farm analysis failed');
    }

    const data = await res.json();
    // Fetch full dashboard details for this analysis
    return await this.getDashboard(data.analysis_id);
  },

  // Get Dashboard by ID
  async getDashboard(analysisId) {
    const res = await fetch(`${API_BASE_URL}/dashboard/${analysisId}`);
    if (!res.ok) {
      throw new Error('Failed to retrieve analysis dashboard');
    }
    return await res.json();
  },

  // Download PDF report
  getPdfReportUrl(analysisId, lang = 'en') {
    return `${API_BASE_URL}/reports/pdf/${analysisId}?lang=${lang}`;
  },

  // Download CSV report
  getCsvReportUrl(analysisId) {
    return `${API_BASE_URL}/reports/csv/${analysisId}`;
  }
};
