from email.message import EmailMessage

from pydantic import EmailStr
from app.config import settings


# Функция которая проверяет, что это забронил человек, а не бот
def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr,
):
    email = EmailMessage()  # Создаем сообщение

    email["Subject"] = "Подтверждение бронирования"  # Тема письма
    email["From"] = settings.SMTP_USER  # От кого отправляем , с нашей почты
    # Отправляем на почту зарегистрированного юзера, эта инфа у нас есть в бд
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Подтвердите бронирование</h1>
            Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}
        """,
        subtype="html"
    )
    return email
