
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

from pydantic import EmailStr

from app.user.service import UsersService
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # Создадим переменную даты времени, когда истечет этот токен
    # expire - истекать
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})  # в этот словарь добавим ключ со значеним expire
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersService.find_one_or_none(email=email)
    if not user:
        #Если не пользователь,
        # то верни None, но если есть пользователь, тогда проверь совпадение паролей
        # и если пароли не совпадают
        # И если что-то из этого не выполняется то вернется Nones
        return None
    if verify_password(password,user.hashed_password):
        return None
    return user

# from secrets import token_bytes
# from base64 import b64encode
# print(b64encode(token_bytes(32)).decode())