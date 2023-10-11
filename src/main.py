from uagents import Agent, Bureau, Context, Model
from models.models import Message
from protocols import TemperatureFetch, TemperatureAlert
from uagents.setup import fund_agent_if_low
import asyncio

# User input for temperature alert settings
# location = input("Enter Location ")
# min_temp = float(input("Enter Minimum Temperature "))
# max_temp = float(input("Enter Maximum Temperature "))
# mail = input("Enter Email ")

# Create the main agent
mainAgent = Agent(name="mainAgent", seed="mainAgent_seed", endpoint={"http://localhost:8002":{}}, port=8002)

# Fund the main agent if its wallet balance is low
fund_agent_if_low(mainAgent.wallet.address())

# Event handler for the main agent startup
# @mainAgent.on_event("startup")
# async def sendData(ctx: Context) -> None:
#     # Send temperature alert settings to the TemperatureFetch agent
#     await ctx.send(destination=TemperatureFetch.fetch_agent.address, message=Message(message=f"{location} {min_temp} {max_temp} {mail}"))

@mainAgent.on_message(model=Message)
async def sendData(ctx: Context, sender: str, msg: Message) -> None:
    data = msg.message.split(" ")
    location = data[0]
    min_temp = float(data[1])
    max_temp = float(data[2])
    mail = data[3]
    await ctx.send(destination=TemperatureFetch.fetch_agent.address, message=Message(message=f"{location} {min_temp} {max_temp} {mail}"))

# Create a bureau to manage multiple agents
bureau = Bureau()

# Add agents to the bureau
bureau.add(TemperatureFetch.fetch_agent)
bureau.add(TemperatureAlert.temp_alert)
bureau.add(mainAgent)
# Run the bureau
if __name__ == "__main__":
    bureau.run()
