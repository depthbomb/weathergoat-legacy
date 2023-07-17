from pydantic import BaseModel
from src.models.GridpointForecast import GridpointForecast


class GridpointForecastGeoJSON(BaseModel):
    properties: GridpointForecast
