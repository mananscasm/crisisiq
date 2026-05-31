from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(min_length=8)
    role: str = "analyst"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegionOut(BaseModel):
    id: int
    code: str
    state: str
    district: str
    latitude: float
    longitude: float
    population: int

    model_config = {"from_attributes": True}


class RiskFeatures(BaseModel):
    region_code: str
    unemployment_rate: float = Field(ge=0, le=100)
    inflation_rate: float = Field(ge=-10, le=100)
    crime_rate: float = Field(ge=0)
    rainfall_deviation: float = Field(ge=-100, le=100)
    heatwave_days: int = Field(ge=0)
    news_sentiment: float = Field(ge=-1, le=1)
    social_sentiment: float = Field(ge=-1, le=1)
    population_density: float = Field(ge=0)
    poverty_rate: float = Field(ge=0, le=100)


class PredictionOut(BaseModel):
    id: int | None = None
    region_code: str
    risk_score: float
    probability: float
    crisis_category: str
    severity: str
    drivers: dict[str, float]
    created_at: datetime | None = None


class RecommendationOut(BaseModel):
    region_code: str
    category: str
    severity_score: float
    actions: list[str]
    rationale: str


class AlertOut(BaseModel):
    id: int
    title: str
    message: str
    severity: str
    acknowledged: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class MetricOut(BaseModel):
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    created_at: datetime | None = None


class PipelineLogOut(BaseModel):
    pipeline_name: str
    status: str
    records_processed: int
    message: str
    created_at: datetime | None = None
