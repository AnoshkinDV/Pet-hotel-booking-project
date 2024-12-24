from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.user.auth import get_password_hash, authenticate_user, create_access_token
from app.user.chemas import SUserAuth
from app.user.dependencies import get_current_user, get_current_admin_user
from app.user.models import Users
from app.user.service import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация пользователей"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    # если пользователь с таким email существует то функция вернет ошибку, мы не дадим зарегистрироваться
    # далее нужно будет захешировать пароль и добавить его в базу данных
    # И нам нужно для проверки существующего юзера обратиться к бд через service
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user:  # если пользователь уже зарегистрирован , то дай ошибку
        raise UserAlreadyExistsException
    # Окей пользователя нет, дальше нам нужно захешировать пароль и добавить в бд
    hashed_password = get_password_hash(user_data.password)
    # Теперь нам нужно добавить пользователя(добавление новой строчки в базу данных)
    await UsersService.add_record(email=user_data.email, hashed_password=hashed_password)
    return {"message": "User registered successfully"}


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)  # Она вернет либо None либо пользователя
    if not user:
        raise IncorrectEmailOrPasswordException  # 401 код значит, что пользователь не аутентифицирован
    # Если пользователь есть, то нужно создать jwt токен и отправить ему в cookies
    access_token = create_access_token({"sub": str(user.id)})
    # Как созданный токен поместить в cookies
    # В фасапи можно работать с запросом пользователя, так и с ответом, который мы пошлем
    # Пропишем responce, и мы может засетить какую нибудь куку в ответе
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response:Response):
    response.delete_cookie("booking_access_token")
    return "Пользователь вышел из системы"

@router.get("/me")
async def read_users_me(
        current_users:Users = Depends(get_current_user)
):
    return current_users

# @router.get("/all")
# async def read_users_all(
#         current_user: Users = Depends(get_current_admin_user)
# ):
#     return current_user