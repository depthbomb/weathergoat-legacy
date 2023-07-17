from pydantic import BaseModel


class RelativeLocation(BaseModel):
    city: str
    state: str
