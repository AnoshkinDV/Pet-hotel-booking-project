import asyncio
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from datetime import date, datetime, timedelta
from pydantic import parse_obj_as
from fastapi_cache.decorator import cache

from app.hotels.schemas import SHotels
from app.hotels.service import HotelsService
from app.service.base import BaseService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("/{location}")
@cache(expire=30)
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}")
):
    await asyncio.sleep(3)
    if not date_from or not date_to:
        raise HTTPException(status_code=400, detail='Пропущены параметры: date_to или date_from')
    hotels = await HotelsService.find_all(location, date_from, date_to)

    hotels_json = parse_obj_as(List[SHotels], hotels) # Приведём hotels через Pydantic провалидируем и убедимся
    # что такое тип есть у pydantic
    return hotels_json # Вернётся список отелей List[SHotels], который потом конвертируется в JSON

