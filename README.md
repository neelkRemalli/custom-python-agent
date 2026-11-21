# Custom Python Agent

A beginner-friendly Python agent using the OpenAI Responses API and function tools.

## Requirements

- Python 3.10+
- An OpenAI API key

## Setup

Create and activate a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

On Windows, activate it with:

    .venv\Scripts\activate

Install dependencies and configure the environment:

    pip install -r requirements.txt

Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.

## Run

    python main.py

## Available tools

- `calculator`
- `get_current_time`

## Tests

    pytest -v
