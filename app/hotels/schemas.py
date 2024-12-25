from typing import List

from pydantic import BaseModel, Json, ConfigDict


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)
