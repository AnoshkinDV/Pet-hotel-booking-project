import datetime
from datetime import timezone, datetime

from app.exceptions import TokenAbsentException, TokenExpiredException, IncorrectFormatTokenException, \
    UserIsNotPresentException, UserIdNotPresentException
from app.user.models import Users
from app.user.service import UsersService
from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )

    except JWTError:
        raise IncorrectFormatTokenException
    current_time = datetime.now(timezone.utc).timestamp()
    expire = payload.get("exp")
    if (not expire) or (
            int(expire) < current_time):  # если время не прошло, то есть меньше текущего времени
        raise TokenExpiredException
    user_id: int = payload.get("sub")
    if not user_id:
        raise UserIdNotPresentException
    user = await UsersService.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    return await UsersService.find_all()
