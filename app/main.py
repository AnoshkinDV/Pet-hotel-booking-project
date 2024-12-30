from contextlib import asynccontextmanager

from fastapi import FastAPI
from typing import AsyncIterator

from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.user.router import router as router_users
from app.booking.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.pages.router import router as router_pages
from app.images.router import router as router_images
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")
# StatiFiles это отдельное приложение

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)

# Добавление площадок, которые могут обращаться к нашему api
origins = [
    "http://localhost:8080"
]
# "https://api.mysite.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Отвечает за куки,и если тру то с каждым запросом посылается кука
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],  # Какие методы мы можем использовать
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)



#1ое событие startup - отвечает за запуск приложения, те при запуске приложения функция startup прогонятся
#2ое собитие shutdown - отвечает за выключение приложения

@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

# uvicorn app.main:app --reload
