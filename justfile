[private]
default:
    @just --list

fmt:
    uv run ruff check --select=I --fix
    uv run ruff format

coverage:
    uv run pytest --cov src --cov-report term-missing
    uv run interrogate -vv

check:
    uv run pytest
    uv run mypy --strict src tests
    uv run ruff check
    uv run ruff format --check
