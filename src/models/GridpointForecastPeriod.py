from pydantic import Field, BaseModel


class GridpointForecastPeriod(BaseModel):
    number: int
    name: str
    start_time: str = Field(alias="startTime")
    end_time: str = Field(alias="endTime")
    is_daytime: bool = Field(alias="isDaytime")
    icon: str
    short_forecast: str = Field(alias="shortForecast")
    detailed_forecast: str = Field(alias="detailedForecast")
