from datetime import date

from fastapi import HTTPException
from fastapi.logger import logger
from sqlalchemy import select, and_, or_, func, insert, delete

from app.datebase import async_session_maker, engine

from app.booking.models import Bookings
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService


class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to >= date_from
                        )
                    )
                )
            ).cte("booked_rooms")
            get_quantity_free_rooms = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("quantity_free_rooms")
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            # print(get_quantity_free_rooms.compile(engine,compile_kwargs={"literal_binds": True}))
            # logger.debug(get_quantity_free_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

            quantity_free_rooms = await session.execute(get_quantity_free_rooms)
            print(quantity_free_rooms.scalar())

            if quantity_free_rooms != 0:
                get_price = select(Rooms.price).where(Rooms.id == room_id)
                price_per_room = await session.execute(get_price)
                price_per_room: int = price_per_room.scalar()  # собираем скаляр, который используется для извлечения
                # первого значения из рез-та запроса
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_to=date_to,
                    date_from=date_from,
                    price=price_per_room
                ).returning(
                    Bookings
                )
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def delete_record(cls, id: int, user_id: int):
        """
        Удаляет запись по `booking_id` и `user_id`.
        """
        async with async_session_maker() as session:
            query = delete(cls.model).where(
                cls.model.id == id,
                cls.model.user_id == user_id
            )
            result = await session.execute(query)
            await session.commit()

            # Проверяем, была ли запись удалена
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Booking not found")