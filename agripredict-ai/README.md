# AgriPredict AI — Smart Crop Planning & Financial Risk Prediction System

> **"Plan Smarter. Grow Better. Reduce Agricultural Risk."**

AgriPredict AI is an AI-powered agricultural web application that helps Indian farmers reduce financial losses by predicting crop suitability, identifying weather-related risks, recommending suitable sowing periods, and estimating cultivation costs and returns.

## Features

- 🌾 **Crop Suitability Prediction** — ML-based crop recommendations using soil, weather, and season data
- 🌧️ **Weather Risk Assessment** — Historical analysis + forecast-based risk evaluation
- 💰 **Financial Estimator** — Cultivation cost, revenue, and profit/loss scenarios
- 📊 **Interactive Dashboard** — Charts, maps, and visual analytics
- 🌍 **Bilingual Support** — English and Telugu interface
- 📄 **Report Generation** — Downloadable PDF/CSV reports
- 🔄 **Demo Mode** — Works offline with sample data

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite, Tailwind CSS, Recharts, React Leaflet |
| Backend | Python, FastAPI, Pydantic |
| Database | SQLite (SQLAlchemy ORM) |
| ML/AI | Scikit-learn, Pandas, NumPy |
| Weather | Open-Meteo API |

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
python -m app.main
```

Backend runs at: http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

### Initialize Database & Train Models

```bash
cd backend
python scripts/initialize_database.py
python scripts/seed_demo_data.py
python scripts/train_models.py
```

## Environment Variables

Copy `.env.example` to `.env` in both `frontend/` and `backend/` directories.

## Demo Scenario

Use the "Sample Farm Data" button to load:
- **Location**: Chittoor District, Andhra Pradesh
- **Land**: 2 acres, Red soil
- **Irrigation**: Rain-fed
- **Season**: Kharif

## Disclaimer

All predictions, recommendations, and financial estimates are illustrative and based on available data. Actual agricultural outcomes depend on numerous factors including local conditions, crop management, weather events, and market dynamics. This tool is intended to support decision-making, not replace professional agricultural advice.

## License

MIT License — Built for hackathon demonstration purposes.
