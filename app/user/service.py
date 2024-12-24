from app.service.base import BaseService
from app.user.models import Users


class UsersService(BaseService):
    model = Users

    @classmethod
    def find_all(cls, **kwargs):
        pass