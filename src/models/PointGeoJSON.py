from pydantic import BaseModel
from src.models.Point import Point


class PointGeoJSON(BaseModel):
    properties: Point
