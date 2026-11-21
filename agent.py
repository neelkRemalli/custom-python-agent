from config import load_settings
from history import ConversationHistory
from llm_client import LLMClient
from tools import TOOL_SCHEMAS, execute_tool


INSTRUCTIONS = """
You are a helpful AI assistant.

You can use tools when they are useful.
Never invent tool results.
Use tools only for their intended purposes.
Explain results clearly and concisely.
"""


class Agent:
    """Coordinate model responses, bounded tool calls, and conversation state."""

    def __init__(self) -> None:
        self.settings = load_settings()
        self.client = LLMClient(self.settings)
        self.history = ConversationHistory()

    def run(self, user_message: str) -> str:
        self.history.add_user_message(user_message)

        for _ in range(self.settings.max_tool_rounds):
            response = self.client.generate(
                instructions=INSTRUCTIONS,
                input_items=self.history.get_input(),
                tools=TOOL_SCHEMAS,
            )
            output = getattr(response, "output", None)
            if not isinstance(output, (list, tuple)):
                raise RuntimeError("OpenAI response contained invalid output.")
            self.history.add_response_items(list(output))

            tool_calls = [item for item in output if getattr(item, "type", None) == "function_call"]
            if not tool_calls:
                return getattr(response, "output_text", None) or "No response generated."

            for call in tool_calls:
                name = getattr(call, "name", None)
                arguments = getattr(call, "arguments", None)
                call_id = getattr(call, "call_id", None)
                if not isinstance(name, str) or not isinstance(arguments, str) or not isinstance(call_id, str):
                    raise RuntimeError("OpenAI response contained a malformed tool call.")
                result = execute_tool(name, arguments)
                self.history.items.append({
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": result,
                })

        return "I reached the maximum tool-call limit."
