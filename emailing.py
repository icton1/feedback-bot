from telegram.message import Message
import smtplib
from email.message import EmailMessage

smtp_server = "smtp.yandex.com"
server_email = "itmo.best.telegram.bot@yandex.ru"
server_password = "PUT YOUR PASSWORD HERE"
eqc_email = "PUT EMAIL HERE"


def send_to_eqc(message: Message):
    email_message = EmailMessage()
    email_message.set_content(message)
    email_message['Subject'] = f'Отзыв на преподавателя'
    email_message['From'] = server_email
    email_message['To'] = eqc_email

    with smtplib.SMTP_SSL(smtp_server, port=465) as server:
        server.login(server_email, server_password)
        server.send_message(email_message)
