from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import parse_obj_as
from app.booking.service import BookingService
from app.booking.schemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.service.base import BaseService
from app.user.dependencies import get_current_user
from app.user.models import Users
from app.tasks.tasks import send_booking_confirmation_email

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
async def get_bookings(
        user: Users = Depends(get_current_user)
) -> list[SBooking]:
    return await BookingService.find_all(user_id=user.id)


@router.post("")
async def add_booking(
        background_tasks: BackgroundTasks,
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user)
):
    new_booking = await BookingService.add(user.id, room_id, date_from, date_to)
    parse_new_booking = parse_obj_as(SBooking, new_booking).dict()

    # Вариант с celery
    # send_booking_confirmation_email.delay(parse_new_booking, user.email)
    # Вариант встроенный background_tasks
    background_tasks.add_task(
        send_booking_confirmation_email, parse_new_booking, user.email)
    if not new_booking:
        raise RoomCannotBeBooked
    return parse_new_booking


@router.delete("/{booking_id}")
async def remove_booking(
        booking_id: int,
        current_user: Users = Depends(get_current_user),
):
    await BookingService.delete_record(id=booking_id, user_id=current_user.id)
