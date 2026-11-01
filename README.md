# Product Management API

A RESTful API built with FastAPI for managing products and tracking their modification history. The application includes business logic for price validation and a filtering system for banned phrases.

## Capabilities

* Create, Read, Update, and Delete (CRUD) operations for products and banned phrases.
* Product modification history tracking (capturing old and new values for updated fields).
* Automatic price validation based on predefined product categories (Electronics, Books, Clothing).
* Product name validation to prevent the use of dynamically managed banned phrases.
* PostgreSQL database integration using SQLAlchemy.

## Architecture and Design Principles

The project follows a layered architecture, where each layer has a single, clearly defined role:

```
app/
├── routers/       # HTTP layer – endpoints, request/response models, dependency wiring
├── services/      # Business logic – validation, banned phrases, change history
├── repositories/  # Data access – all SQLAlchemy queries and persistence
├── models.py      # ORM models (database tables)
└── schemas.py     # Pydantic schemas (API contracts and input validation)
```

A request flows strictly in one direction: **Router → Service → Repository → Database**.

## Prerequisites

* Docker and Docker Compose (recommended)
* Python 3.13+ and `uv` package manager (for local development)

## Installation and Running (Docker)

The easiest way to run the application is using Docker.

1. Clone the repository and open the terminal in the root directory.
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

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/products` | List all products |
| `GET` | `/api/v1/products/{id}` | Get a product by ID |
| `GET` | `/api/v1/products/{id}/history` | Get the modification history of a product |
| `POST` | `/api/v1/products` | Create a product |
| `PUT` | `/api/v1/products/{id}` | Update a product (partial updates supported) |
| `DELETE` | `/api/v1/products/{id}` | Delete a product |
| `GET` | `/api/v1/banned-phrases` | List all banned phrases |
| `POST` | `/api/v1/banned-phrases` | Add a banned phrase |
| `PUT` | `/api/v1/banned-phrases/{id}` | Update a banned phrase |
| `DELETE` | `/api/v1/banned-phrases/{id}` | Delete a banned phrase |

### Validation rules

* Product name: 3–20 alphanumeric characters, unique, must not contain any banned phrase (case-insensitive).
* Quantity: integer, not less than 0.
* Price limits per category:

| Category | Min price (PLN) | Max price (PLN) |
|----------|-----------------|-----------------|
| `Elektronika` | 50 | 50 000 |
| `Ksiazka` | 5 | 500 |
| `Odziez` | 10 | 5 000 |

## Example Usage

**Create a product**

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 3999.99, "category": "Elektronika", "quantity": 10}'
```

```json
{
  "name": "Laptop",
  "price": 3999.99,
  "category": "Elektronika",
  "quantity": 10,
  "id": 1,
  "created_at": "2026-11-02T10:00:00Z"
}
```

**Update a product** – only the fields you send are changed:

```bash
curl -X PUT http://localhost:8000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 3499.99, "quantity": 8}'
```

**Get the modification history** – every changed field is recorded with its old and new value:

```bash
curl http://localhost:8000/api/v1/products/1/history
```

```json
[
  {
    "id": 1,
    "id_product": 1,
    "variable_name": "price",
    "old_value": "3999.99",
    "new_value": "3499.99",
    "created_at": "2026-11-02T10:05:00Z"
  },
  {
    "id": 2,
    "id_product": 1,
    "variable_name": "quantity",
    "old_value": "10",
    "new_value": "8",
    "created_at": "2026-11-02T10:05:00Z"
  }
]
```

**Banned phrases in action**

```bash
curl -X POST http://localhost:8000/api/v1/banned-phrases \
  -H "Content-Type: application/json" \
  -d '{"name": "fake"}'

curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name": "FakeWatch", "price": 199, "category": "Elektronika"}'
```

```json
{ "detail": "The product name contains banned phrase: 'fake'." }
```

**Price outside the category limit**

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Notebook", "price": 2, "category": "Ksiazka"}'
```

Returns `422 Unprocessable Entity` with the message: `For category Ksiazka, the price must be between 5.0 and 500.0 PLN.`

## Running Tests

To run the automated test suite using pytest, execute the following command in your terminal:

```bash
uv run pytest
```