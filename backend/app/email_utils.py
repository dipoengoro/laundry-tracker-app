import smtplib
import asyncio
from email.message import EmailMessage
from app.config import settings as env


async def send_email(subject: str, recipient: str, body: str):
    message = EmailMessage()
    message["From"] = env.MAIL_FROM
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body, subtype='html')

    loop = asyncio.get_event_loop()

    await loop.run_in_executor(None, lambda: smtplib.SMTP(env.MAIL_SERVER, env.MAIL_PORT).send_message(message))