from pydantic import BaseModel
from src.models.RelativeLocation import RelativeLocation


class RelativeLocationGeoJSON(BaseModel):
    properties: RelativeLocation
