from openai import OpenAI


class LLMClient:
    """Thin wrapper around the OpenAI Responses API."""

    def __init__(self, settings) -> None:
        self.client = OpenAI(api_key=settings.api_key)
        self.model = settings.model

    def generate(self, instructions, input_items, tools):
        try:
            return self.client.responses.create(
                model=self.model,
                instructions=instructions,
                input=input_items,
                tools=tools,
            )
        except Exception as exc:
            raise RuntimeError(f"OpenAI API request failed: {exc}") from exc
