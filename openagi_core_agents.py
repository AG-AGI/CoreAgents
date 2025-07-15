import re
import requests
from typing import Callable, List, Any, Dict

def function_tool(func: Callable) -> Callable:
    func._is_tool = True
    return func

def ask(prompt: str) -> str:
    url = "http://text.pollinations.ai/"
    encoded = prompt.replace(" ", "%20").replace("\n", "%0A")
    response = requests.get(url + encoded)
    return response.text

class Agent:
    def __init__(self, name: str, instructions: str, model: str, tools: List[Callable]):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = {tool.__name__: tool for tool in tools if getattr(tool, "_is_tool", False)}

    def run_tool(self, tool_name: str, *args, **kwargs) -> Any:
        tool = self.tools.get(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found")
        return tool(*args, **kwargs)

    def respond(self, input_text: str) -> str:
        tool_list = ", ".join(self.tools.keys())
        prompt = (
            f"Agent name: {self.name}\n"
            f"Instructions: {self.instructions}\n"
            f"Available tools: {tool_list}\n"
            f"User input: {input_text}\n"
            f"Respond in the format:\n"
            f"TOOL:tool_name:param1,param2,...\n"
            f"or direct answer if no tools needed.\n"
            f"Begin:"
        )

        response = ask(prompt)

        while True:
            tool_call = self._parse_tool_call(response)
            if tool_call is None:
                return response.strip()
            tool_name, tool_args = tool_call
            try:
                tool_result = self.run_tool(tool_name, *tool_args)
            except Exception as e:
                tool_result = f"Error running tool {tool_name}: {e}"

            prompt = (
                f"Agent name: {self.name}\n"
                f"Instructions: {self.instructions}\n"
                f"Tool result: {tool_result}\n"
                f"Continue responding in haiku form without further tool calls."
            )
            response = ask(prompt)

    def _parse_tool_call(self, text: str):
        match = re.search(r"TOOL:(\w+):([\w\s,]+)", text)
        if not match:
            return None
        tool_name = match.group(1)
        params_str = match.group(2).strip()
        params = [p.strip() for p in params_str.split(",")] if params_str else []
        return tool_name, params
