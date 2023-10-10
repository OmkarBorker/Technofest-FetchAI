from uagents import Agent, Bureau, Context, Model
from uagents.setup import fund_agent_if_low

from models.models import Message

from mail.mail import MailSender

from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

def check_temp(temp, min_temp, max_temp) -> str:
    """
    Check if the given temperature is outside the specified range.

    Args:
    - temp (float): The current temperature.
    - min_temp (float): The minimum temperature threshold.
    - max_temp (float): The maximum temperature threshold.

    Returns:
    - str: A message indicating whether the temperature is out of range.
    """
    if temp < min_temp:
        msg = f"Temperature is below minimum threshold ({min_temp} °C): {temp} °C"
    elif temp > max_temp:
        msg = f"Temperature is above maximum threshold ({max_temp} °C): {temp} °C"
    else:
        msg = None
    return msg

# Create an instance of the temp_alert agent
temp_alert = Agent(name="temp_alert", seed="temp_alert_seed", endpoint=["http://localhost:8001"], port=8001)

# Fund the agent if its wallet balance is low
fund_agent_if_low(temp_alert.wallet.address())

# Define message handling for the temp_alert agent
@temp_alert.on_message(model=Message)
async def displayTempAlert(ctx: Context, sender: str, msg: Message) -> None:
    # Extract temperature data from the message
    temp_data = msg.message.split(" ")
    temp_data = [float(temp_data[0]), float(temp_data[1]), float(temp_data[2]), temp_data[3]]
    
    # Extract receiver email
    receiver_mail = temp_data[3]

    # Check if the temperature is out of range
    alert = check_temp(temp_data[0], temp_data[1], temp_data[2])

    # If the temperature is out of range, send an email alert
    if alert is not None:
        mail_sender = MailSender(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            smtp_password=os.getenv("SMTP_PASSWORD"),
            sender_email=os.getenv("SENDER_EMAIL")
        )
        try:
            await mail_sender.send_email(subject='Temperature Alert', body=f"Temperature Alert: {alert}", receiver_email=receiver_mail)
        except Exception as e:
            ctx.logger.error(f"Failed to send email: {str(e)}")
        ctx.logger.info(f"Temperature Alert: {alert}")
    else:
        ctx.logger.info("Temperature is within range")
