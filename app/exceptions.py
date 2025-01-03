from fastapi import HTTPException, status


class BookingException(HTTPException):  # <-- наследуемся от HTTPException,который наследован от Exception
    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Некорректная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен пользователя истёк"


# Ошибка по отсутствию токена
class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectFormatTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Некорректный формат токена"


class UserIdNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "ID пользователя нет в JWT токене"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователя с таким id нет в БД"


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"
