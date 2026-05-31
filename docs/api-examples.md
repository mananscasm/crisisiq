# API Examples

## Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@crisisiq.ai","password":"CrisisIQ@123"}'
```

## Predict Risk

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "region_code":"BR-PAT",
    "unemployment_rate":12.6,
    "inflation_rate":7.9,
    "crime_rate":76,
    "rainfall_deviation":-28,
    "heatwave_days":16,
    "news_sentiment":-0.41,
    "social_sentiment":-0.46,
    "population_density":1823,
    "poverty_rate":28
  }'
```

## Analytics

```bash
curl http://localhost:8000/api/v1/analytics/overview -H "Authorization: Bearer $TOKEN"
```

## Live Top-50 City Risk

```bash
curl "http://localhost:8000/api/v1/realtime/risk/top50?limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

## Live City Detail

```bash
curl http://localhost:8000/api/v1/realtime/cities/IN-MUM \
  -H "Authorization: Bearer $TOKEN"
```
