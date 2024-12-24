
from fastapi import FastAPI, Query
from typing import Optional
from datetime import date

from pydantic import BaseModel, Field


from app.user.router import router as router_users
from app.booking.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
# @app.get("/hotels/{hotel_id}")
# def get_hotels(hotel_id: int, date_from, date_to):
#     return hotel_id,date_from, date_to
app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)



class HotelaSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            has_spa: Optional[bool] = None,
            stars: Optional[int] = Query(None, ge=1, le=5)
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


class SHotel(BaseModel):
    adress: str
    name: str
    stars: Optional[int] = Field(None, ge=1, le=5)


# @app.get("/hotels")
# def get_hotels(
#         location: str,
#         date_from: date,
#         date_to: date,
#         has_spa: Optional[bool] = None,
#         stars: Optional[int] = Query(None, ge=1, le=5)
# ) -> list[SHotel]:
#     hotels = [
#         {
#             "adress": "ул.Васенко, 2, Саранск",
#             "name": "Bad Hotel",
#             "stars": 1,
#
#         },
#     ]
#     return hotels

# @app.get("/hotels")
# def get_hotels(
#   search_args: HotelaSearchArgs = Depends()
# ):
#     return search_args

# uvicorn app.main:app --reload


