from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.hotels.rooms.router import get_rooms_by_time
from app.hotels.rooms.schemas import SRoomInfo
from app.hotels.router import get_hotels_by_location_and_time

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/hotels")
async def get_hotels_pages(
        request: Request,
        hotels = Depends(get_hotels_by_location_and_time)
):
    return templates.TemplateResponse(name="hotels.html",
                                      context={"request":request,
                                               "hotels":hotels}) #ответим шаблоном,
    # добавим имя и context где обязательно должен быть request

from fastapi import Query
from datetime import date, timedelta, datetime
from typing import List

@router.get("/hotels/{hotel_id}/rooms", name="get_rooms_page")
async def get_rooms_page(
    hotel_id: int,
    request: Request,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
    rooms: List[SRoomInfo] = Depends(get_rooms_by_time)
):
    return templates.TemplateResponse(
        name="rooms.html",
        context={
            "request": request,
            "rooms": rooms,
            "hotel_id": hotel_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )