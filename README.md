# CrisisIQ

CrisisIQ is an AI-driven socio-economic crisis prediction platform for Indian states and districts. It includes a FastAPI backend, Next.js 15 dashboard, ML training pipeline, Airflow DAG, MLflow tracking, PostgreSQL schemas, Redis-ready orchestration, Docker Compose, Kubernetes manifests, and CI.

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

Demo login:

- Email: `admin@crisisiq.ai`
- Password: `CrisisIQ@123`

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

## Train Models

```bash
cd crisisiq
pip install -r ml/requirements.txt
python ml/training/train_models.py
```

The training script compares Logistic Regression, Random Forest, AdaBoost, and XGBoost, logs metrics to `mlruns`, writes `ml/reports/model_metrics.csv`, and saves the best model at `ml/models/crisis_risk_model.joblib`.

## Real-Time India City APIs

The backend includes live-data endpoints for India's top 50 cities:

- `GET /api/v1/realtime/cities`
- `GET /api/v1/realtime/cities/IN-MUM`
- `GET /api/v1/realtime/risk/top50?limit=50`
- `GET /api/v1/analytics/overview/live`

Live sources:

- Open-Meteo for current weather, temperature, precipitation, and heatwave/rainfall stress.
- GDELT 2.1 for city-specific news headlines and lightweight sentiment scoring, with Google News RSS fallback when GDELT rate-limits.
- CrisisIQ city baselines for unemployment, inflation, crime, poverty, population density, and demographics where real-time official city feeds are not available.

## Folder Map

- `backend/app`: FastAPI app, SQLAlchemy models, auth, services, REST routes.
- `backend/pipelines`: ingestion, cleaning, and feature engineering modules.
- `frontend`: Next.js 15 TypeScript dashboard with Tailwind, Recharts, Leaflet, and lucide icons.
- `ml/training`: classical ML and LSTM training scripts.
- `airflow/dags`: scheduled pipeline DAG.
- `infra/nginx`: reverse proxy config.
- `k8s`: Kubernetes manifests.
- `docs`: architecture and API examples.
- `datasets`: seed/demo data.

## Deployment

- Frontend: deploy `frontend/` to Vercel with `NEXT_PUBLIC_API_BASE`.
- Backend: deploy `backend/Dockerfile` to Render, ECS, Cloud Run, or EC2.
- Database: use Supabase, RDS, or Cloud SQL and set `DATABASE_URL`.
- ML services: run training through Airflow, GitHub Actions, or a scheduled container.
- HTTPS: terminate TLS at Vercel, a cloud load balancer, or the Kubernetes ingress.

## Caveat

The included dataset is synthetic/demo-scale for portfolio use. Do not use generated scores for real emergency, policing, welfare, credit, or government decisions without audited data provenance, bias testing, human oversight, and domain validation.
