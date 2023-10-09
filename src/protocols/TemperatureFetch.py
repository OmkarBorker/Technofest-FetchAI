import requests
from uagents import Agent, Context, Bureau, Model
from uagents.protocol import Protocol
from uagents.setup import fund_agent_if_low
from .TemperatureAlert import temp_alert
from models.models import ListMessage,Message

class TemperatureAlertAgent(Agent):
    def __init__(self, name: str, seed: str, location: str, api_key: str, endpoint:str, port:int, min_temp:float, max_temp:float):
        super().__init__(name=name, seed=seed, endpoint=endpoint, port=port)
        self.location = location
        self.api_key = api_key
        self.min_temp = min_temp
        self.max_temp = max_temp
    async def get_temperature(self) -> float:
        import requests
        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.location}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()
            temp = data["main"]["temp"]
            return temp
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch temperature data: {str(e)}")
    
    async def display_temperature(self,ctx:Context) ->str:
        temp = await self.get_temperature()
        await ctx.send(destination=temp_alert.address, message= Message(message = f"{temp} {self.min_temp} {self.max_temp}"))
        return f"Temperature in {self.location} is {temp}°C"  

fetch_agent = TemperatureAlertAgent(name="fetch_agent", seed="alert_agent_seed", location=input("Enter Location "), api_key="a74eebe6704ebe9ae5aed50998769d85",  endpoint=["http://localhost:8000"],port=8000, min_temp = float(input("Enter Minimum Temperature ")), max_temp = float(input("Enter Maximum Temperature ")))
fund_agent_if_low(fetch_agent.wallet.address())
@fetch_agent.on_interval(5.0)
async def display(ctx: Context):
    msg = await fetch_agent.display_temperature(ctx)
    ctx.logger.info(msg)
if __name__ == "__main__":
    fetch_agent.run()
