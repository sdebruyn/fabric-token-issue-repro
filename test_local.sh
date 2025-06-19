#!/usr/bin/env sh

uv venv
uv pip install -r requirements.txt
uv run python test_sql_token.py
