from uagents import Agent, Bureau, Context, Model
from uagents.setup import fund_agent_if_low

from models.models import Message

def check_temp(temp, min_temp, max_temp) -> str:
    if temp < min_temp:
        msg = f"Temperature is below minimum threshold ({min_temp}): {temp}"
    elif temp > max_temp:
        msg = f"Temperature is above maximum threshold ({max_temp}): {temp}"
    return msg


temp_alert = Agent(name="temp_alert", seed="temp_alert_seed", endpoint =["http://localhost:8001"], port=8001)
fund_agent_if_low(temp_alert.wallet.address())
@temp_alert.on_message(model = Message)
async def displayTempAlert(ctx: Context,sender:str, msg: Message) -> None:
    temp = msg.message.split(" ")
    temp = [float(i) for i in temp]
    alert = check_temp(temp[0], temp[1], temp[2])
    if alert is not None:
        ctx.logger.info(f"Temperature Alert: {alert}")
    else:
        ctx.logger.info("Temperature is within range")

