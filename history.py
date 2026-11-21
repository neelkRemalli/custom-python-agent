from typing import Any


class ConversationHistory:
    """Store the input items exchanged during one agent conversation."""

    def __init__(self) -> None:
        self.items: list[dict[str, Any]] = []

    def add_user_message(self, message: str) -> None:
        self.items.append({"role": "user", "content": message})

    def add_response_items(self, items: list[Any]) -> None:
        self.items.extend(items)

    def get_input(self) -> list[Any]:
        return self.items

    def clear(self) -> None:
        self.items.clear()
