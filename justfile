[private]
default:
    @just --list

install:
    poetry install
    poetry shell

fmt:
    ruff check --select=I --fix
    ruff format

coverage:
    python -m pytest --cov dahlia --cov-report term-missing
    interrogate -vv

check:
    python -m pytest
    mypy --strict dahlia tests
    ruff check
    ruff format --check
