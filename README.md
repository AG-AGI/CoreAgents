# CoreAgents

`openagi_core_agents` is a minimal Python module to create agentic AI with tool-using capabilities powered by an LLM. It enables defining **function tools** and an **Agent** that can intelligently decide when to call tools based on natural language input, then combine the tool outputs with generated responses — all while following custom instructions like responding in haiku form.

## Features

- Easy-to-use `@function_tool` decorator to mark Python functions as callable tools.
- `Agent` class that integrates tools and an LLM to dynamically decide how and when to invoke tools.
- Supports multi-step reasoning: the agent can call tools, get results, and continue generating responses.
- Flexible instruction support, e.g., always respond in haiku form.
- Example integration with a simple HTTP-based text generation API. (you can replace it with any LLM API by editing the `ask` function in `openagi_core_agents.py`)

## License

MIT

## Example 

``` python

from openagi_core_agents import Agent, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Agent",
    instructions="You're a helpful assistant.",
    tools=[get_weather,],
)

agent.debug_tools()

print(agent.respond("What's the weather in Tokyo?"))

```
