from openagi_core_agents import Agent, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="pollinations",
    tools=[get_weather],
)

print(agent.respond("What's the weather in Toronto?"))
