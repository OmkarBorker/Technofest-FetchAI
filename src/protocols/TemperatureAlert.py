from uagents import Agent, Bureau, Context, Model
from uagents.setup import fund_agent_if_low

from models.models import Message

from mail.mail import MailSender

def check_temp(temp, min_temp, max_temp) -> str:
    if temp < min_temp:
        msg = f"Temperature is below minimum threshold ({min_temp} °C): {temp} °C"
    elif temp > max_temp:
        msg = f"Temperature is above maximum threshold ({max_temp} °C): {temp} °C"
    return msg


temp_alert = Agent(name="temp_alert", seed="temp_alert_seed", endpoint =["http://localhost:8001"], port=8001)
fund_agent_if_low(temp_alert.wallet.address())

@temp_alert.on_message(model = Message)
async def displayTempAlert(ctx: Context,sender:str, msg: Message) -> None:
    temp = msg.message.split(" ")
    temp = [float(i) for i in temp]
    alert = check_temp(temp[0], temp[1], temp[2])
    if alert is not None:
        mail_sender = MailSender(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            smtp_password="",
            sender_email=""
        )
        try:
            await mail_sender.send_email(subject='Temperature Alert', body=f"Temperature Alert: {alert}", receiver_email='')
        except Exception as e:
            ctx.logger.error(f"Failed to send email: {str(e)}")
        ctx.logger.info(f"Temperature Alert: {alert}")
    else:
        ctx.logger.info("Temperature is within range")

