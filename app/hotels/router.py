from datetime import date
from typing import List, Optional
from fastapi import APIRouter, HTTPException

from app.hotels.schemas import SHotels
from app.hotels.service import HotelsService
from app.service.base import BaseService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/{location}")
async def get_hotels_by_location_and_time(
        location: str,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
) -> list[SHotels]:
    if not date_from or not date_to:
        raise HTTPException(status_code=400, detail='Пропущены параметры: date_to или date_from')
    hotels = await HotelsService.find_all(location,date_from,date_to)
    return hotels
