import requests
from uagents import Agent, Context, Bureau, Model
from uagents.protocol import Protocol
from uagents.setup import fund_agent_if_low
from .TemperatureAlert import temp_alert
from models.models import ListMessage, Message

from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

class TemperatureAlertAgent(Agent):
    def __init__(self, name: str, seed: str, api_key: str, endpoint: str, port: int):
        """
        Initialize the TemperatureAlertAgent.

        Args:
        - name (str): The name of the agent.
        - seed (str): The seed for generating the agent's wallet.
        - api_key (str): The API key for accessing temperature data.
        - endpoint (str): The endpoint for the agent.
        - port (int): The port for the agent.
        """
        super().__init__(name=name, seed=seed, endpoint=endpoint, port=port)
        self.api_key = api_key
        self.location=""

    def storeData(self, location: str, min_temp: float, max_temp: float, mail: str) -> None:
        """
        Store temperature-related data for the agent.

        Args:
        - location (str): The location for which temperature data is stored.
        - min_temp (float): The minimum temperature threshold.
        - max_temp (float): The maximum temperature threshold.
        - mail (str): The email address for temperature alerts.
        """
        self.location = location
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.mail = mail

    async def get_temperature(self, location) -> float:
        """
        Fetch the current temperature for a given location using the OpenWeatherMap API.

        Args:
        - location (str): The location for which to fetch the temperature.

        Returns:
        - float: The current temperature in Celsius.
        """
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            temp = data["main"]["temp"]
            return temp
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch temperature data: {str(e)}")

    async def display_temperature(self, ctx: Context) -> str:
        """
        Display the current temperature for the stored location.

        Args:
        - ctx (Context): The context for the agent.

        Returns:
        - str: A message indicating the current temperature.
        """
        temp = await self.get_temperature(self.location)
        ctx.logger.info(f"Temperature in {self.location} is {temp} °C")
        await ctx.send(destination=temp_alert.address, message=Message(message=f"{temp} {self.min_temp} {self.max_temp} {self.mail}"))
        return f"Temperature in {self.location} is {temp} °C"

# Create an instance of the TemperatureAlertAgent
fetch_agent = TemperatureAlertAgent(name="fetch_agent", seed="alert_agent_seed", api_key=os.getenv("OPW"), endpoint={"http://localhost:8000":{}}, port=8000)

# Fund the agent if its wallet balance is low
fund_agent_if_low(fetch_agent.wallet.address())

# Define message handling for the agent
@fetch_agent.on_message(model=Message)
async def receive(ctx: Context, sender: str, msg: Message) -> None:
    data = msg.message.split(" ")
    location = data[0]
    min_temp = float(data[1])
    max_temp = float(data[2])
    mail = data[3]
    fetch_agent.storeData(location, min_temp, max_temp, mail)

# Define periodic temperature display
@fetch_agent.on_interval(3.0)
async def display(ctx: Context):
    msg = await fetch_agent.display_temperature(ctx)

# Run the agent
if __name__ == "__main__":
    fetch_agent.run()
