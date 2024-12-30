# """
# Конфигурационный файл для подключения Celery
# """
from celery import Celery
from app.config import settings


celery_app = Celery(
    "tasks",  # название
    # указываем брокер сообщений, который будет хранить эти сообщения
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.tasks"]  # указываем celery, где будут храниться задачи
)
