from uagents import Agent, Bureau, Context, Model

from protocols import TemperatureFetch, TemperatureAlert

bureau = Bureau()
bureau.add(TemperatureFetch.fetch_agent)
bureau.add(TemperatureAlert.temp_alert)
if __name__ == "__main__":
    bureau.run()