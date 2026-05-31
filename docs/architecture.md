# CrisisIQ Architecture

CrisisIQ is organized as a production-style monorepo with a Next.js intelligence dashboard, FastAPI backend, PostgreSQL persistence, Redis-ready asynchronous processing, MLflow model tracking, Airflow orchestration, and Docker/Kubernetes deployment assets.

## Data Flow

1. Ingestion modules collect census, economic, crime, climate, news, and social sentiment inputs.
2. Cleaning modules validate schema, normalize numeric ranges, and impute missing values.
3. Feature engineering creates economic stress, climate stress, sentiment distress, and structural vulnerability indicators.
4. Training scripts compare Logistic Regression, Random Forest, AdaBoost, and XGBoost, logging metrics to MLflow.
5. FastAPI serves authenticated predictions, analytics, recommendations, alerts, regions, and pipeline status.
6. The dashboard visualizes heatmaps, forecasts, SHAP-style drivers, alerts, and scenario simulation.

## Production Notes

- Replace the demo CSV with governed source connectors before operational use.
- Store `JWT_SECRET`, database credentials, webhook URLs, and provider API keys in a managed secret store.
- Use RDS/Supabase for PostgreSQL, ElastiCache/Redis Cloud for Redis, Vercel for frontend, and ECS/EKS/GKE/Render for services.
- Use MLflow Model Registry promotion gates with Evidently drift reports before replacing production models.
