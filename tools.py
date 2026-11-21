import ast
import json
import operator
from datetime import datetime, timezone
from typing import Any, Callable


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str) -> int | float:
    """Evaluate a limited arithmetic expression without executing Python."""
    if len(expression) > 500:
        raise ValueError("Expression is too long.")

    def evaluate(node: ast.AST) -> int | float:
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp):
            op = OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError("Unsupported operator.")

            if isinstance(node.op, ast.Pow):
                right = evaluate(node.right)
                if abs(right) > 100:
                    raise ValueError("Exponent too large.")
                left = evaluate(node.left)
                if abs(left) > 1e100:
                    raise ValueError("Number too large.")
                result = op(left, right)
            else:
                result = op(evaluate(node.left), evaluate(node.right))

            if isinstance(result, (int, float)) and abs(result) > 1e100:
                raise ValueError("Number too large.")
            return result

        if isinstance(node, ast.UnaryOp):
            op = OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError("Unsupported operator.")
            return op(evaluate(node.operand))

        raise ValueError("Invalid mathematical expression.")

    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, RecursionError) as exc:
        raise ValueError("Invalid mathematical expression.") from exc
    return evaluate(tree.body)


def get_current_time() -> str:
    """Return the current time in UTC as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


TOOL_SCHEMAS = [
    {
        "type": "function",
        "name": "calculator",
        "description": "Calculate a mathematical expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression.",
                }
            },
            "required": ["expression"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Get the current UTC time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
            "required": [],
        },
        "strict": True,
    },
]

TOOL_REGISTRY: dict[str, Callable[..., Any]] = {
    "calculator": calculate,
    "get_current_time": get_current_time,
}


def execute_tool(name: str, arguments: str) -> str:
    """Validate and execute one registered tool call, returning its result."""
    tool = TOOL_REGISTRY.get(name)
    if tool is None:
        return f"Error: Unknown tool '{name}'."

    try:
        parsed = json.loads(arguments)
        if not isinstance(parsed, dict):
            raise ValueError("Arguments must be a JSON object.")

        if name == "calculator":
            if set(parsed) != {"expression"}:
                raise ValueError("Expected only 'expression'.")
            if not isinstance(parsed["expression"], str):
                raise ValueError("'expression' must be a string.")
        elif name == "get_current_time" and parsed:
            raise ValueError("This tool accepts no arguments.")

        return str(tool(**parsed))
    except (json.JSONDecodeError, TypeError, ValueError, ArithmeticError, OverflowError, RecursionError) as exc:
        return f"Error: {exc}"
