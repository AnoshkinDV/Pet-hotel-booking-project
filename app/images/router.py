import shutil

from PIL.ImagePath import Path
from fastapi import UploadFile, APIRouter
from app.tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)


# тк наша картинка хранится в оперативке, и она нигде на жестком диске не хранится, то ей нужно сохранить в
# в нашу папку через shutil
@router.post("/hotels", status_code=201)
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(im_path)  # отложим задачу
