# Custom Python Agent

A small, command-line AI agent built with Python and the OpenAI Responses API. It demonstrates how an agent sends conversation context to a model, handles function calls, runs registered tools, and returns tool results for a final response.

## Features

- OpenAI Responses API integration
- Multi-turn conversation history
- Bounded model and tool-call loop
- Allowlisted calculator and UTC time tools
- Environment-based configuration with `python-dotenv`
- Focused tests for tool behavior and agent flow

## Project structure

| File | Responsibility |
| --- | --- |
| `main.py` | Command-line entry point and user interaction |
| `agent.py` | Agent orchestration, response handling, and tool dispatch |
| `llm_client.py` | OpenAI API client |
| `history.py` | Conversation input and response history |
| `tools.py` | Tool schemas, argument validation, and implementations |
| `config.py` | Environment loading and settings validation |
| `requirements.txt` | Python dependencies |
| `tests/test_tools.py` | Tool and agent behavior tests |

Agent instructions are currently defined in `agent.py`.

## Requirements

- Python 3.10 or later
- An OpenAI API key

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set the required configuration:

```dotenv
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-6
MAX_TOOL_ROUNDS=5
```

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | API credential used by the OpenAI client; keep it private. |
| `OPENAI_MODEL` | Model sent with Responses API requests. |
| `MAX_TOOL_ROUNDS` | Maximum agent iterations before the loop stops. |

The application loads `.env` from the working directory. Configuration defaults and validation are defined in `config.py`.

## Run

Start the interactive agent from the project root:

```bash
python main.py
```

Enter a request at the `You:` prompt. Type `exit` or `quit` to close the application. End-of-file and Ctrl+C also exit the input loop.

## Available tools

### Calculator

Evaluates supported arithmetic expressions without executing arbitrary Python code. Supported operators include addition, subtraction, multiplication, division, exponentiation, modulo, and unary signs.

Examples: `25 * 4`, `100 / 5`, `2 ** 8`.

### UTC time

Returns the current time in UTC in ISO 8601 format.

## Run tests

```bash
pytest -v
```

The tests do not require a live API call for the mocked agent-flow cases.

## Execution flow

1. Load and validate environment settings.
2. Initialize the OpenAI client and conversation history.
3. Send the current conversation, instructions, and registered tool schemas to the model.
4. Validate and execute returned tool calls.
5. Add tool results to the conversation and continue until a final response is returned or the iteration limit is reached.

The agent dispatches only tools registered in `tools.py`; model output is not executed as Python or shell code.
