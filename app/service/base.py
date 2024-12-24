from sqlalchemy import select, insert, delete, update
from app.datebase import async_session_maker



class BaseService:
    model = None

    # @classmethod
    # async def find_by_id(cls, model_id: int):
    #     async with async_session_maker() as session:
    #         query = select(cls.model.__table__.columns).filter_by(id=model_id)
    #         # cls.model.__table__.columns нужен для отсутствия вложенности в ответе Алхимии
    #         result = await session.execute(query)
    #         return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **kwargs):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add_record(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            # Нам не важно что возвращается, на самом деле тут None
            await session.execute(query)
            # Не забудем сделать session.commit, когда мы делаем select нам не нужен coomit,
            # ведь commit позволяет при запросах на insert update delete зафиксировать изменения в базе данных
            # важно при обновлении данных фиксировать изменения
            await session.commit()

    @classmethod
    async def delete_record(cls,**kwargs):
        async with async_session_maker() as session:
            query = delete(cls.model).where(**kwargs)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_record(cls, **kwargs):
        async with async_session_maker() as session:
            query = update(cls.model).where(**kwargs).values(**kwargs)
            await session.execute(query)
            await session.commit()


