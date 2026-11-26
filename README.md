# Product CRUD API

A Flask API backed by PostgreSQL. Gunicorn serves the API on port 8000 in Docker.

## Run with Docker Compose

Create a `.env` file in the repository root with the following values for local development.

```dotenv
POSTGRES_USER=products
POSTGRES_PASSWORD=products
POSTGRES_DB=products
DATABASE_URL=postgresql://products:products@postgres:5432/products
```

```bash
docker compose up --build -d
curl http://localhost:8000/status
curl http://localhost:8000/products
```

On startup, the app creates the product table and loads sample products if the table is empty.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | Returns a greeting |
| GET | `/status` | Returns the service status |
| GET | `/products` | Lists products |
| GET | `/products/{id}` | Fetches a product |
| POST | `/products` | Adds a product |
| PUT | `/products/{id}` | Updates the product at the path ID |
| DELETE | `/products/{id}` | Deletes a product |

Send a JSON object with `id` (integer), `name` (string), `description` (string), `price` (number), and `quantity` (integer) for POST and PUT.
