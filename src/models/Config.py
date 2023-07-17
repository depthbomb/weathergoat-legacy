from src.utils import is_url_valid
from pydantic import BaseModel, field_validator


class _ForecastZoneConfiguration(BaseModel):
    channel_id: int
    latitude: float
    longitude: float
    radar_image: str

    @field_validator("radar_image")
    def validate_radar_image(cls, v):
        if not is_url_valid(v):
            raise ValueError("must be a valid HTTP/HTTPS URL")

        return v


class _AlertZoneConfiguration(BaseModel):
    channel_id: int
    zone_id: str
    radar_image: str

    @field_validator("radar_image")
    def validate_radar_image(cls, v):
        if not is_url_valid(v):
            raise ValueError("must be a valid HTTP/HTTPS URL")

        return v


class _CleanupConfiguration(BaseModel):
    channel_ids: list[int]


class _WeatherGoatConfiguration(BaseModel):
    token: str
    owner_id: int


class Config(BaseModel):
    weathergoat: _WeatherGoatConfiguration
    cleanup: _CleanupConfiguration
    alert_zones: list[_AlertZoneConfiguration]
    forecast_zones: list[_ForecastZoneConfiguration]