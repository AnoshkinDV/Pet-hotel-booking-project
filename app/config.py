# Здесь будут храниться данные о подключении к бд, от почты, к редису
# Создаем класс с настройками и используем способ импортирования переменных окружения через Pydantic


from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

from pydantic_settings import SettingsConfigDict

load_dotenv()  # Загрузка переменных окружения из файла .env


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )



settings = Settings()
print(settings.SECRET_KEY)
