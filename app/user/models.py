from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.datebase import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Связываем 2 таблицы для sqlalchemy, хоть они и связаны через внешний ключ

    booking = relationship("Bookings", back_populates="user")
