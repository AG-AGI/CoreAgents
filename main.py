from openagi_core_agents import Agent, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    return f"The weather in {city} is sunny"

@function_tool
def get_user_name() -> str:
    """Get the user's name."""
    return "User's name is John Doe"

agent = Agent(
    name="Agent",
    instructions="You're a helpful assistant.",
    tools=[get_weather, get_user_name],
)

agent.debug_tools()

print(agent.respond("What's my name?"))
