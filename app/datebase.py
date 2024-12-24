# В этом файле находится все что связано с БД и её подключением
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL,echo=True)
async_session_maker = async_sessionmaker(engine,expire_on_commit= False) #Создаем генератор сессий, где параметры это движок, асинхронный класс,маркер на истекание сессии


class Base(DeclarativeBase): # Base используется для миграций , все модели hotels,bookings, rooms будут наследоваться от Base, и в этом классе будут аккумилироваться все данные о всех моделях
    #чтобы затем alembic мог сравнить состояние на бэкенде и состояние в бд и создать миграцию
    pass


