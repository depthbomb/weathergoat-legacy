from pydantic import Field, BaseModel
from src.models.RelativeLocationGeoJSON import RelativeLocationGeoJSON


class Point(BaseModel):
    forecast: str
    relative_location: RelativeLocationGeoJSON = Field(alias="relativeLocation")
