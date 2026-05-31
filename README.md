# CrisisIQ

CrisisIQ is an AI-driven socio-economic crisis prediction platform for India's top cities. It combines live weather signals, city-specific news sentiment, socio-economic baselines, machine learning risk scoring, intervention recommendations, and an intelligence-style dashboard for monitoring emerging crisis risk.

## Live Demo

- Frontend: https://frontend-zeta-mauve-19.vercel.app/
- Backend: https://crisisiq-backend.vercel.app
- API health: https://crisisiq-backend.vercel.app/health
- GitHub: https://github.com/mananscasm/crisisiq

Demo credentials:

- Email: `admin@crisisiq.ai`
- Password: `CrisisIQ@123`

## Need for This Project

Socio-economic crises rarely appear from a single source. A city can become vulnerable because unemployment rises, rainfall fails, heatwaves intensify, crime reports increase, inflation pressures households, or public sentiment shifts after local events. These signals are usually scattered across separate dashboards, news feeds, government reports, and weather systems.

CrisisIQ is designed to bring those weak signals into one decision-support platform. The goal is to help analysts, public-policy teams, NGOs, researchers, and emergency planners identify where risk is rising, understand the likely drivers, and prepare targeted interventions before the situation becomes severe.

This project is useful because it demonstrates:

- Early warning intelligence for Indian cities using multiple signal types.
- Real-time monitoring instead of static spreadsheet-only analysis.
- Explainable risk scoring with visible driver impact.
- Intervention recommendations mapped to crisis categories.
- A full-stack, deployable AI platform architecture suitable for a portfolio or proof of concept.

## What Works Now

- Tracks India's top 50 cities.
- Fetches live weather data from Open-Meteo.
- Computes heatwave and rainfall stress indicators.
- Supports city-level news sentiment using GDELT and Google News RSS when requested.
- Uses socio-economic city baselines for unemployment, inflation, crime, poverty, density, and population.
- Generates risk scores, severity labels, driver explanations, and recommendations.
- Provides a live dashboard with search, filters, CSV export, map markers, charts, alerts, and recommendations.
- Exposes authenticated REST APIs with Swagger documentation.

## Real-Time City APIs

The backend includes live-data endpoints for India's top 50 cities:

- `GET /api/v1/realtime/cities`
- `GET /api/v1/realtime/cities/IN-MUM`
- `GET /api/v1/realtime/risk/top50?limit=50`
- `GET /api/v1/realtime/risk/top50?limit=10&include_news=true`
- `GET /api/v1/analytics/overview/live`

Live sources:

- Open-Meteo for current weather, temperature, precipitation, and heatwave/rainfall stress.
- GDELT 2.1 for city-specific news headlines and lightweight sentiment scoring.
- Google News RSS fallback when `include_news=true`.
- CrisisIQ baselines for indicators that do not have reliable real-time city APIs.

## Tech Stack

- Frontend: Next.js 15, TypeScript, Tailwind CSS, Recharts, Leaflet, lucide-react.
- Backend: FastAPI, Python, SQLAlchemy, JWT authentication, SlowAPI rate limiting.
- Data/ML: Pandas, NumPy, Scikit-learn, XGBoost, SHAP-ready model layer, MLflow, DVC.
- Pipelines: Airflow DAG structure, ingestion, cleaning, and feature engineering modules.
- Infra: Docker Compose, Dockerfiles, Nginx reverse proxy, Kubernetes manifests, GitHub Actions.
- Deployment: Vercel frontend and backend, GitHub Pages workflow included for static frontend hosting.

## Architecture

```text
Live Sources
  Open-Meteo weather
  GDELT / Google News RSS
  City socio-economic baselines
        |
        v
FastAPI Backend
  Auth
  Realtime city risk service
  Prediction service
  Recommendation engine
  Analytics APIs
        |
        v
Next.js Dashboard
  India heatmap
  Risk cards
  Driver charts
  Alerts
  Recommendations
  Search/filter/export
```

## Quick Start

```bash
cd crisisiq
docker compose up --build
```

Open:

- Frontend: http://localhost:3000
- Backend Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health
- MLflow: http://localhost:5000

## Local Backend

```bash
cd crisisiq/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Local Frontend

```bash
cd crisisiq/frontend
npm install
npm run dev
```

Set the frontend API URL when needed:

```bash
NEXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
```

On Windows PowerShell:

```powershell
$env:NEXT_PUBLIC_API_BASE="http://localhost:8000/api/v1"
npm run dev
```

## Train Models

```bash
cd crisisiq
pip install -r ml/requirements.txt
python ml/training/train_models.py
```

The training script compares Logistic Regression, Random Forest, AdaBoost, and XGBoost, logs metrics to `mlruns`, writes `ml/reports/model_metrics.csv`, and saves the best model at `ml/models/crisis_risk_model.joblib`.

## Sample API Usage

Login:

```bash
curl -X POST https://crisisiq-backend.vercel.app/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@crisisiq.ai","password":"CrisisIQ@123"}'
```

Fetch top city risks:

```bash
curl "https://crisisiq-backend.vercel.app/api/v1/realtime/risk/top50?limit=50" \
  -H "Authorization: Bearer $TOKEN"
```

Fetch detailed live risk for Mumbai:

```bash
curl https://crisisiq-backend.vercel.app/api/v1/realtime/cities/IN-MUM \
  -H "Authorization: Bearer $TOKEN"
```

## Folder Map

- `backend/app`: FastAPI app, SQLAlchemy models, auth, services, REST routes.
- `backend/pipelines`: ingestion, cleaning, and feature engineering modules.
- `frontend`: Next.js dashboard with Tailwind, Recharts, Leaflet, and live controls.
- `ml/training`: classical ML and LSTM training scripts.
- `airflow/dags`: scheduled pipeline DAG.
- `infra/nginx`: reverse proxy config.
- `k8s`: Kubernetes manifests.
- `docs`: architecture and API examples.
- `datasets`: seed/demo data.

## Deployment

Current deployment:

- Frontend: Vercel
- Backend: Vercel Python serverless function
- Backend storage: SQLite in `/tmp` for demo/serverless runtime

Alternative/free frontend deployment:

- GitHub Pages workflow is included at `.github/workflows/pages.yml`.
- Enable GitHub Pages in repository settings and choose GitHub Actions as the source.

Production recommendations:

- Move backend persistence to Supabase, Neon, RDS, or Cloud SQL.
- Store secrets in a managed secret store.
- Add scheduled ingestion jobs for official government datasets.
- Add observability, API quotas, and model drift monitoring.
- Use a persistent worker platform for heavier news and ML jobs.

## Important Limitations

CrisisIQ is a portfolio-grade proof of concept, not an official emergency system. Real-time weather and news signals are live, but unemployment, inflation, crime, poverty, density, and population are currently city baselines because reliable real-time official city-level APIs are not generally available.

Do not use generated scores for real emergency, policing, welfare, credit, or government decisions without audited data provenance, bias testing, human oversight, domain validation, and clear accountability.
