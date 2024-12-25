# """
# Конфигурационный файл для подключения Celery
# """
from celery import Celery

celery_app = Celery(
    "tasks",  # название
    broker="redis://localhost:6379",  # указываем брокер сообщений, который будет хранить эти сообщения
    include=["app.tasks.tasks"]  # указываем celery, где будут храниться задачи
)
