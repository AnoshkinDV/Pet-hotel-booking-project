from sqladmin import ModelView
from .user.models import Users
from .booking.models import Bookings


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    can_delete = False
    column_details_exclude_list = ['hashed_password']
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.columns]
    # can_delete = False
    # column_details_exclude_list = ['hashed_password']
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-calendar"
