from pydantic import BaseModel
from src.models.GridpointForecastPeriod import GridpointForecastPeriod


class GridpointForecast(BaseModel):
    periods: list[GridpointForecastPeriod]
