import json
from types import SimpleNamespace

import pytest

from agent import Agent
from tools import calculate, execute_tool


def test_calculator():
    assert calculate("2 + 3 * 4") == 14


def test_calculator_power():
    assert calculate("2 ** 3") == 8


def test_calculator_rejects_unsafe_expression():
    with pytest.raises(ValueError):
        calculate("import os")


def test_calculator_bounds_large_result():
    assert "Number too large" in execute_tool("calculator", '{"expression":"10 ** 100 * 10"}')


def test_unknown_tool():
    assert "Unknown tool" in execute_tool("unknown", "{}")


def test_malformed_json():
    assert "Error" in execute_tool("calculator", "{invalid")


def test_invalid_arguments():
    assert "Error" in execute_tool("calculator", "{}")


def test_division_by_zero():
    assert "Error" in execute_tool("calculator", '{"expression":"1 / 0"}')


def test_time_tool():
    assert "T" in execute_tool("get_current_time", "{}")


def test_tool_rejects_extra_arguments():
    result = execute_tool("get_current_time", json.dumps({"unexpected": 1}))
    assert "Error" in result


def test_agent_final_response(monkeypatch):
    class FakeClient:
        def __init__(self, settings):
            pass

        def generate(self, **kwargs):
            return SimpleNamespace(output=[], output_text="Hello!")

    monkeypatch.setattr("agent.load_settings", lambda: SimpleNamespace(max_tool_rounds=2))
    monkeypatch.setattr("agent.LLMClient", FakeClient)
    assert Agent().run("Hello") == "Hello!"


def test_agent_executes_tool(monkeypatch):
    function_call = SimpleNamespace(
        type="function_call", name="calculator", arguments='{"expression":"2 + 3"}', call_id="call_123"
    )
    tool_response = SimpleNamespace(output=[function_call], output_text="")
    final_response = SimpleNamespace(output=[], output_text="The result is 5.")

    class FakeClient:
        def __init__(self, settings):
            self.responses = [tool_response, final_response]

        def generate(self, **kwargs):
            return self.responses.pop(0)

    monkeypatch.setattr("agent.load_settings", lambda: SimpleNamespace(max_tool_rounds=2))
    monkeypatch.setattr("agent.LLMClient", FakeClient)
    assert Agent().run("Calculate 2 + 3") == "The result is 5."


def test_agent_stops_at_round_limit(monkeypatch):
    function_call = SimpleNamespace(
        type="function_call", name="calculator", arguments='{"expression":"1 + 1"}', call_id="call_1"
    )

    class FakeClient:
        def __init__(self, settings):
            pass

        def generate(self, **kwargs):
            return SimpleNamespace(output=[function_call], output_text="")

    monkeypatch.setattr("agent.load_settings", lambda: SimpleNamespace(max_tool_rounds=2))
    monkeypatch.setattr("agent.LLMClient", FakeClient)
    agent = Agent()
    assert agent.run("Keep calculating") == "I reached the maximum tool-call limit."


def test_agent_reports_api_errors(monkeypatch):
    class FakeClient:
        def __init__(self, settings):
            pass

        def generate(self, **kwargs):
            raise RuntimeError("API request failed")

    monkeypatch.setattr("agent.load_settings", lambda: SimpleNamespace(max_tool_rounds=1))
    monkeypatch.setattr("agent.LLMClient", FakeClient)
    with pytest.raises(RuntimeError, match="API request failed"):
        Agent().run("Hello")
