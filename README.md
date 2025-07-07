# Cobertura Pae Backend

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

This repository contains the backend for the PAE Cobertura project, built with FastAPI.

## Prerequisites

- Python 3.10+
- Poetry
- Docker (optional, for running the database)

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd pae-cobertura
    ```

2.  **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root directory by copying the `.env.example` file (if it exists) or by creating it from scratch. It should contain the database connection string.
    ```
    DATABASE_URL="postgresql://user:password@localhost:5434/pae_cobertura"
    ```

## Running the Application

You can run the application using the following Poe the Poet task:

```bash
poetry run poe dev
```

This will start the Uvicorn server with hot-reloading enabled.

## Database

This project uses `Alembic` for database migrations and `SQLModel` as the ORM.

### Migrations

To create a new migration based on your model changes, run:

```bash
poetry run poe db-generate -m "Your migration message"
```

To apply the migrations to the database, run:

```bash
poetry run poe db-migrate
```
*Note: The `db-generate` command is a shortcut for `alembic revision --autogenerate` and `db-migrate` is a shortcut for `alembic upgrade head`.*

### Database Seeding

To populate the database with initial data, run:

```bash
poetry run poe db-seed
```

## Development

### Commits

This project uses [Commitizen](http://commitizen.github.io/cz-cli/) for standardized commit messages. To commit your changes, please use the following commands:

```bash
git add .
poetry run cz commit
```

This will prompt you to fill out the required commit fields.

### Changelog

The `CHANGELOG.md` is automatically generated based on the commits.

To create the changelog for the first time for a specific version:
```bash
poetry run cz changelog --unreleased-version "v0.1.0"
```

To update the changelog with new commits:
```bash
poetry run cz changelog
```

### Linting

To run the linters and formatters configured with `pre-commit`, execute:

```bash
poetry run poe lint
```
