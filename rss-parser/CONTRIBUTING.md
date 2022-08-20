# Contributing

## Install requirements

We need:

- **docker**: with docker-compose
- **pyenv**: with specific python version installed
- **poetry**: latest version
- **make**: to automate tasks

Install all dependencies with:

```bash
poetry install
```

Activate virtualenv with if not activated already:

```bash
poetry shell
```

Setup your IDE to this **.venv**.

## Pull Requests

Before create pull request:

- `make lint`: check project with **mypy** and **flake8**
- `make test`: run tests
