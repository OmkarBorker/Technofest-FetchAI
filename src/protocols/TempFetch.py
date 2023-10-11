from typing import List
from uagents import Agent, Context, Bureau, Model,Protocol
from models.models import Message
import requests
import os
from dotenv import load_dotenv
from mail.mail import MailSender

load_dotenv()

class Fetch(Model):
    min_temp: float
    max_temp: float
    mail: str   
    location: str

class Response(Model):
    temp: float
    location: str

fetch_proto = Agent(name = "fetch_proto", seed = "fetch_proto_seed", endpoint = ["http://127.0.0.1:8000/get"], port = 8000)

@fetch_proto.on_message(model= Message, replies=Message)
async def fetch_temp(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg}")
    msg = msg.message.split(" ")
    location = msg[0]
    min_temp = float(msg[1])
    max_temp = float(msg[2])
    mail = msg[3]
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={os.getenv('OPW')}&units=metric"
    mail_sender = MailSender(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        smtp_password=os.getenv("SMTP_PASSWORD"),
        sender_email=os.getenv("SENDER_EMAIL")
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        ctx.logger.info(f"{os.getenv('SMTP_PASSWORD')},{os.getenv('SENDER_EMAIL')}")
        if temp < min_temp:
            msg = f"Temperature is below minimum threshold ({min_temp} °C): {temp} °C"
            mail_sender.send_email(
                receiver_email=mail,
                subject="Temperature Alert",
                body=msg
            )
        elif temp > max_temp:
            msg = f"Temperature is above maximum threshold ({max_temp} °C): {temp} °C"
            mail_sender.send_email(
                receiver_email=mail,
                subject="Temperature Alert",
                body=msg
            )
        else:
            msg = None
        await ctx.send(destination=sender, message=Message(message = msg))
    except Exception as e:
        ctx.logger.error(f"Failed to fetch temperature data: {str(e)}")

if __name__ == "__main__":
    fetch_proto.run()