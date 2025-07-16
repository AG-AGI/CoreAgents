import re
import requests
import urllib.parse
from typing import Callable, List, Any, Dict, Tuple, Optional

def function_tool(func: Callable) -> Callable:
    func._is_tool = True
    return func

def ask(prompt: str) -> str:
    print("\n>>> Sending Prompt to LLM:\n" + "="*20 + f"\n{prompt}\n" + "="*20)
    encoded_prompt = urllib.parse.quote(prompt, safe='')
    try:
        response = requests.get(f"http://text.pollinations.ai/{encoded_prompt}")
        response.raise_for_status()
        text_response = response.text
        print(f"\n<<< Received LLM Response:\n" + "="*20 + f"\n{text_response}\n" + "="*20)
        return text_response
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with LLM API: {e}")
        return f"Error: Could not get a response from the model. Details: {e}"

class Agent:
    def __init__(self, name: str, instructions: str, tools: List[Callable]):
        self.name = name
        self.instructions = instructions
        self.tools = {tool.__name__: tool for tool in tools if getattr(tool, "_is_tool", False)}

    def run_tool(self, tool_name: str, args: List[str]) -> Any:
        tool = self.tools.get(tool_name)
        if not tool:
            return f"Error: Tool '{tool_name}' not found."
        try:
            return tool(*args)
        except Exception as e:
            return f"Error running tool {tool_name} with args {args}: {e}"

    def respond(self, user_input: str) -> str:
        history = [f"User Input: {user_input}"]
        
        for _ in range(5):
            tool_descriptions = "\n".join([f"- {name}: {func.__doc__.strip() if func.__doc__ else 'No description available.'}" for name, func in self.tools.items()])
            
            prompt = (
                f"You are {self.name}, an AI assistant. Follow these instructions: {self.instructions}\n\n"
                f"Conversation History:\n{''.join(history)}\n\n"
                f"Available Tools:\n{tool_descriptions}\n\n"
                f"Based on the conversation, decide if you need to use a tool. "
                f"If a tool is needed, respond ONLY in the format: TOOL:tool_name:arg1,arg2,...\n"
                f"If no tool is needed, provide a direct, final answer to the user. \n"
                f"Begin:"
            )

            response = ask(prompt)
            
            tool_call = self._parse_tool_call(response)

            if tool_call:
                tool_name, tool_args = tool_call
                history.append(f"\nTool Call: {tool_name}({', '.join(tool_args)})")
                
                tool_result = self.run_tool(tool_name, tool_args)
                
                history.append(f"\nTool Result: {tool_result}")
            else:
                return response.strip()
        
        return "Error: Agent reached maximum iterations without providing a final answer."

    def _parse_tool_call(self, text: str) -> Optional[Tuple[str, List[str]]]:
        tool_names = "|".join(self.tools.keys())
        match = re.search(rf"(?:TOOL:)?({tool_names}):(.*)", text.strip(), re.DOTALL)
        if not match:
            return None
        
        tool_name = match.group(1).strip()
        params_str = match.group(2).strip()
        
        if params_str:
            params = [p.strip() for p in params_str.split(",")]
        else:
            params = []
            
        return tool_name, params

    def debug_tools(self):
        print("\n--- Available Tools for Agent '{}' ---".format(self.name))
        if not self.tools:
            print("No tools available.")
            return
        for name, func in self.tools.items():
            doc = func.__doc__
            description = doc.strip() if doc else "No description available."
            print(f"- Name: {name}")
            print(f"  Description: {description}")
        print("-------------------------------------\n")
