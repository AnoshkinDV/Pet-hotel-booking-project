from fastapi import FastAPI, Query
from typing import Optional
from datetime import date
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.user.router import router as router_users
from app.booking.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.pages.router import router as router_pages
from app.images.router import router as router_images
from fastapi.middleware.cors import CORSMiddleware

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
#"https://api.mysite.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Отвечает за куки,и если тру то с каждым запросом посылается кука
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"], #Какие методы мы можем использовать
    allow_headers=["Content-Type","Set-Cookie","Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)


# uvicorn app.main:app --reload
