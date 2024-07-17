[private]
default:
    @just --list

fmt:
    poetry run ruff check --select=I --fix
    poetry run ruff format

coverage:
    poetry run python -m pytest --cov dahlia --cov-report term-missing
    poetry run interrogate -vv

check:
    poetry run python -m pytest
    poetry run mypy --strict dahlia tests
    poetry run ruff check
    poetry run ruff format --check
