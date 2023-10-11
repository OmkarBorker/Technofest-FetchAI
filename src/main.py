from uagents import Agent,Bureau, Context, Model
from uagents.setup import fund_agent_if_low
import requests
import json
from protocols.TempFetch import fetch_proto, Fetch
from models.models import Message

mainAgent = Agent(name="mainAgent", seed="mainAgent_seed", endpoint=["http://127.0.0.1:8001/submit"], port=8001)

fund_agent_if_low(mainAgent.wallet.address())

def read_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file: {str(e)}")
        return {} 

DATA = Fetch(location = "Mumbai", min_temp = 10, max_temp = 20, mail = "aryanshrivastav603@gmail.com")

mainAgent._storage.set("DATA", DATA.dict())

@mainAgent.on_interval(10)
async def sendData(ctx:Context):
    storage_file = "src/data/data.json"
    try:
        data = read_from_json(storage_file)
        ctx.logger.info(f"Read data from file: {data}")

        # Process the data as needed
        # For example, send a message to fetch_proto
        await ctx.send(destination=fetch_proto.address, message=Message(message=f"{data['location']} {data['min_temp']} {data['max_temp']} {data['email']}"))
    except FileNotFoundError:
        ctx.logger.warning(f"File {storage_file} not found.")


@mainAgent.on_message(model=Message)
async def receive(ctx: Context, sender: str, msg: Message) -> None:
    ctx.logger.info(f"Received message from {sender}: {msg}")
    requests.post("http://127.0.0.1:5000", {"message": msg.message})


bureau = Bureau()
bureau.add(fetch_proto)
bureau.add(mainAgent)

if __name__ == "__main__":
    bureau.run() 
