from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import current_user
from app.models.domain import User
from app.services.realtime_sources import RealtimeCityService, RealtimeDataError
from app.services.top_cities import TOP_50_CITIES

router = APIRouter(prefix="/realtime", tags=["realtime"])
service = RealtimeCityService()


@router.get("/cities")
def cities(_: User = Depends(current_user)) -> list[dict]:
    return [
        {
            "code": city.code,
            "city": city.city,
            "state": city.state,
            "latitude": city.latitude,
            "longitude": city.longitude,
            "population_millions": city.population_millions,
        }
        for city in TOP_50_CITIES
    ]


@router.get("/cities/{code}")
async def city_realtime_risk(code: str, _: User = Depends(current_user)) -> dict:
    try:
        return await service.city_risk(code)
    except RealtimeDataError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/risk/top50")
async def top50_realtime_risk(
    limit: int = Query(default=50, ge=1, le=50),
    include_news: bool = Query(default=False),
    _: User = Depends(current_user),
) -> list[dict]:
    rows = await service.top50(limit=limit, include_news=include_news)
    return sorted(rows, key=lambda item: item["risk_score"], reverse=True)
