from openagi_core_agents import Agent, function_tool

@function_tool
def dice_roll(sides: int = 6) -> int:
    """Roll a dice with the specified number of sides."""
    import random
    sides = int(sides)
    return random.randint(1, sides)

agent = Agent(
    name="Agent",
    instructions="You're a helpful assistant.",
    tools=[dice_roll],
)

agent.debug_tools()

print(agent.respond("Roll a dice with 6 sides."))
