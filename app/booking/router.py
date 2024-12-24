from datetime import date

from fastapi import APIRouter, Depends
from app.booking.service import BookingService
from app.booking.schemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.service.base import BaseService
from app.user.dependencies import get_current_user
from app.user.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
async def get_bookings(
        user: Users = Depends(get_current_user)
) -> list[SBooking]:
    # print(user, type(user),user.id, user.email, user.hashed_password )
    return await BookingService.find_all(user_id=user.id)


@router.post("")
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user)
):
    new_booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not new_booking:
        raise RoomCannotBeBooked


@router.delete("/{booking_id}")
async def remove_booking(
        booking_id: int,
        current_user: Users = Depends(get_current_user),
):
    await BookingService.delete_record(id=booking_id, user_id=current_user.id)