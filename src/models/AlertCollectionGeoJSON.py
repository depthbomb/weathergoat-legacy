from pydantic import BaseModel
from src.models.GeoJSONFeature import GeoJSONFeature


class AlertCollectionGeoJSON(BaseModel):
    features: list[GeoJSONFeature]
