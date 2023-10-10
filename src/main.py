from uagents import Agent, Bureau, Context, Model
from models.models import Message
from protocols import TemperatureFetch, TemperatureAlert
from uagents.setup import fund_agent_if_low
import asyncio

location = input("Enter Location ")
min_temp = float(input("Enter Minimum Temperature "))
max_temp = float(input("Enter Maximum Temperature "))

mainAgent = Agent(name="mainAgent", seed="mainAgent_seed", endpoint =["http://localhost:8002"], port=8002)
fund_agent_if_low(mainAgent.wallet.address())
@mainAgent.on_event("startup")
async def sendData(ctx: Context) -> None:
    await ctx.send(destination=TemperatureFetch.fetch_agent.address, message= Message(message = f"{location} {min_temp} {max_temp}"))

bureau = Bureau()
bureau.add(TemperatureFetch.fetch_agent)
bureau.add(TemperatureAlert.temp_alert)
bureau.add(mainAgent)
if __name__ == "__main__":
    # location = input("Enter Location ")
    # min_temp = float(input("Enter Minimum Temperature "))
    # max_temp = float(input("Enter Maximum Temperature "))
    # asyncio.run(sendData(mainAgent, Message(message = f"{location} {min_temp} {max_temp}")))
    bureau.run()