from pydantic import BaseModel
from src.models.Alert import Alert


class GeoJSONFeature(BaseModel):
    properties: Alert
