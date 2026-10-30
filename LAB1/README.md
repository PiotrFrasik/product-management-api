# Product Management API

A RESTful API built with FastAPI for managing products and tracking their modification history. The application includes business logic for price validation and a filtering system for banned phrases.

## Capabilities

* Create, Read, Update, and Delete (CRUD) operations for products and banned phrases.
* Product modification history tracking (capturing old and new values for updated fields).
* Automatic price validation based on predefined product categories (Electronics, Books, Clothing).
* Product name validation to prevent the use of dynamically managed banned phrases.
* PostgreSQL database integration using SQLAlchemy.

## Prerequisites

* Docker and Docker Compose (recommended)
* Python 3.10+ and `uv` package manager (for local development)

## Installation and Running (Docker)

The easiest way to run the application is using Docker.

1. Extract the project archive and open the terminal in the root directory.
2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at `http://localhost:8000`.
4. You can access the interactive Swagger UI documentation at `http://localhost:8000/docs`.

## Local Installation

If you prefer to run the API directly on your machine:

1. Ensure a PostgreSQL server is running and configure the `DATABASE_URL` in the `.env` file.
2. Install dependencies using the `uv` package manager:
   ```bash
   uv sync
   ```
3. Start the FastAPI development server:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

## Running Tests

To run the automated test suite using pytest, execute the following command in your terminal:

```bash
uv run pytest
```