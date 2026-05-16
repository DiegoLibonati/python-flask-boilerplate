# Python Flask Api Boilerplate

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

> **Want a MongoDB version?** Check out [`python-flask-mongo-api-boilerplate`](https://github.com/DiegoLibonati/python-flask-mongo-api-boilerplate) — the same boilerplate adapted to work with MongoDB and PyMongo.

## Description

**Python Flask Api Boilerplate** is a production-ready starting point for building REST APIs with **Flask**, designed to eliminate the repetitive setup and architectural decisions that come with every new backend project.

**What it is:** A starting point — not a framework — for developers who want to spin up a Flask API without rebuilding the same infrastructure from scratch each time. Every layer, pattern, and tooling choice is already wired together and working.

**The problem it solves:** Starting a Flask API from zero means making the same decisions repeatedly: how to structure layers, how to handle errors globally, how to validate input, how to configure environments, how to set up Docker, linting, tests, and security audits. This boilerplate makes all those decisions once, so you can focus on building the actual product.

**The example resource:** The boilerplate ships with a fully functional `note` resource that manages a simple list of named entries stored **in memory**. It demonstrates every layer of the architecture (Blueprint → Controller → Service → DAO) without requiring any external database. When you're ready to connect a real database, you only need to replace the DAO layer — everything else stays the same.

**What it includes:**

- **Layered architecture** enforced by convention: Blueprint → Controller → Service → DAO → In-Memory Store. Each layer has a single responsibility and only talks to the one directly below it.
- **Pydantic v2** for request validation and data serialization, with a custom `exceptions_decorator` decorator that automatically converts `ValidationError` into structured JSON API responses — no try/catch boilerplate in controllers.
- **Custom exception hierarchy** (`ValidationAPIError`, `NotFoundAPIError`, `ConflictAPIError`, `InternalAPIError`) that produces consistent error responses across the entire API.
- **Environment-based configuration** using a `DefaultConfig` base class extended by `DevelopmentConfig`, `TestingConfig`, and `ProductionConfig`, loaded dynamically by the app factory.
- **Docker** setup for development and production, with a multi-stage Dockerfile for slim production images.
- **Gunicorn** as the production WSGI server, configured via `gunicorn_config.py`.
- **Ruff** for fast linting and formatting, and **mypy** for static type checking, both enforced automatically via **pre-commit** hooks on every commit.
- **pip-audit** integration for scanning production dependencies against known vulnerability databases.
- **GitHub Actions CI** pipeline that runs lint, type checking, security audit, and tests on every push and pull request.
- **pytest** configured and organized to mirror the `src/` structure.
- **Startup initialization** layer (`src/startup/`) for seeding default data when the app boots.

**How to use it:** Clone the repository, bring up the Docker environment, and replace the `note` resource (blueprint, controller, service, DAO, model, constants) with your own domain logic. The architecture, tooling, and error handling are already in place — you only write what's unique to your application.

## Technologies used

1. Python 3.11 -> Flask
2. Docker
3. Gunicorn

## Libraries used

#### Runtime (`[project.dependencies]`)

```
flask==3.1.3
pydantic==2.11.9
gunicorn==23.0.0
```

#### Dev (`[project.optional-dependencies]` dev)

```
pre-commit==4.3.0
pip-audit==2.7.3
ruff==0.11.12
mypy==1.13.0
```

#### Test (`[project.optional-dependencies]` test)

```
pytest==8.4.2
pytest-env==1.1.5
pytest-cov==4.1.0
pytest-timeout==2.3.1
pytest-xdist==3.5.0
```

## Getting Started

With the stack in mind, here's how to bring the project up locally. The recommended path is Docker; the local virtual environment is for running tooling that doesn't need the full container (pre-commit, tests, security audit).

### With Docker

1. Clone the repository
2. Copy `.env.example` to `.env` and adjust the values if needed (see [Env Keys](#env-keys))
3. Stand inside the repository folder and execute: `docker-compose -f dev.docker-compose.yml build --no-cache`
4. Once built, execute: `docker-compose -f dev.docker-compose.yml up --force-recreate`

NOTE: You have to be standing in the folder containing `dev.docker-compose.yml` and you need to install **Docker Desktop** if you are on Windows.

### Local Virtual Environment

Used by [Pre-Commit](#pre-commit-for-development), [Testing](#testing), and [Security Audit](#security-audit) when you want to run them outside the container.

> **Python version:** The project requires **Python 3.11**. The `.python-version` file pins this for tools like `pyenv`. Make sure your local interpreter matches before creating the virtual environment.

1. Stand inside the repository folder
2. Execute: `python -m venv venv`
3. Activate it:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Execute: `pip install -e .`
5. Execute: `pip install -e ".[dev]"`
6. Execute: `pip install -e ".[test]"`

### Pre-Commit for Development

Pre-commit runs Ruff lint/format and mypy type checking on every commit. Install it inside the activated virtual environment.

1. Activate the virtual environment (see [Local Virtual Environment](#local-virtual-environment))
2. Execute: `pre-commit install`
3. Every commit will now run the configured hooks. To run them manually across the repo: `pre-commit run --all-files`

## Env Keys

The Docker setup and the Flask app read configuration from `.env`. These are the variables it expects.

1. `TZ`: Refers to the timezone setting for the container.
2. `HOST`: Refers to the network interface where the backend API listens (e.g., 0.0.0.0 to allow external connections).
3. `PORT`: Refers to the port on which the backend API is exposed.
4. `MAX_CONTENT_LENGTH`: Maximum allowed request body size in bytes (default: `1048576` = 1 MB). Requests exceeding this limit are rejected by Flask before reaching any controller.
5. `SEED_DEFAULT_DATA`: When `true`, the app seeds default data into the in-memory store on startup. Useful for development and manual testing.

```ts
TZ=America/Argentina/Buenos_Aires

HOST=0.0.0.0
PORT=5050
MAX_CONTENT_LENGTH=1048576

SEED_DEFAULT_DATA=false
```

## Project Structure

With the app running, here's how the codebase is organized. The folder layout mirrors the layered architecture described in the next section.

```
python-flask-api-boilerplate/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── blueprints/
│   │   ├── routes.py
│   │   └── v1/
│   │       ├── health_bp.py
│   │       └── note_bp.py
│   ├── configs/
│   │   ├── default_config.py
│   │   ├── development_config.py
│   │   ├── production_config.py
│   │   ├── testing_config.py
│   │   ├── gunicorn_config.py
│   │   └── logger_config.py
│   ├── controllers/
│   │   ├── health_controller.py
│   │   └── note_controller.py
│   ├── services/
│   │   └── note_service.py
│   ├── data_access/
│   │   └── note_dao.py
│   ├── models/
│   │   └── note_model.py
│   ├── constants/
│   │   ├── codes.py
│   │   ├── messages.py
│   │   └── defaults.py
│   ├── startup/
│   │   └── init_notes.py
│   └── utils/
│       ├── exceptions.py
│       ├── exceptions_decorator.py
│       └── helpers.py
├── tests/
│   └── __init__.py
├── app.py
├── wsgi.py
├── Dockerfile.development
├── Dockerfile.production
├── dev.docker-compose.yml
├── prod.docker-compose.yml
├── requirements.txt
├── requirements.test.txt
├── requirements.dev.txt
├── pyproject.toml
├── .editorconfig
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
└── README.md
```

1. `src` -> Root directory of the source code. Contains the full application logic following a **layered architecture** pattern.
2. `configs` -> Contains all **configuration classes** organized by environment (development, production, testing). Includes logging setup and server settings.
3. `blueprints` -> Defines **API routes and endpoints**. Organized by API version (`v1/`) to support versioning.
4. `controllers` -> Handles **HTTP request/response logic**. Receives requests from blueprints and delegates business logic to services.
5. `services` -> Contains **business logic and rules**. Validates data, enforces constraints, and orchestrates operations between controllers and the data access layer.
6. `data_access` -> Implements the **Repository/DAO pattern**. Abstracts all data operations, making it easy to swap the underlying storage (in-memory, SQL, NoSQL) without affecting other layers.
7. `models` -> Defines **Pydantic models** for data validation and serialization.
8. `constants` -> Holds **static values** like error codes, user messages, and default data.
9. `startup` -> Contains **initialization logic** executed when the application starts, such as seeding default data.
10. `utils` -> Contains **shared utilities** including custom exceptions, the `exceptions_decorator` error handling decorator, and helper functions.
11. `tests` -> Contains **tests** organized to mirror the `src/` structure.
12. `app.py` -> The **application factory**. Creates and configures the Flask app instance using the Factory pattern.
13. `wsgi.py` -> The **production entry point** for WSGI servers like Gunicorn.
14. `Dockerfile.*` -> Docker configurations for **development and production** environments.
15. `requirements.txt` -> Lists **production dependencies**.
16. `requirements.test.txt` -> Lists **testing dependencies** (pytest, pytest-env, etc.).
17. `requirements.dev.txt` -> Lists **development dependencies** (pre-commit, pip-audit, etc.).
18. `pyproject.toml` -> **Unified project configuration** for pytest, ruff, and project metadata.

## Architecture & Design Patterns

### Layered Architecture

This project follows a **Layered Architecture** pattern, organizing code into distinct levels with clear responsibilities. Each layer only communicates with the layer directly below it.

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│                  (Blueprints & Controllers)                 │
│            Handles HTTP requests and responses              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      BUSINESS LAYER                         │
│                        (Services)                           │
│          Contains business logic and validations            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA ACCESS LAYER                       │
│                         (DAO)                               │
│            Abstracts data storage operations                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATA STORE                            │
│                  (In-Memory / Database)                     │
└─────────────────────────────────────────────────────────────┘
```

#### Benefits

- **Separation of Concerns**: Each layer has a single responsibility
- **Testability**: Layers can be tested independently
- **Maintainability**: Changes in one layer don't affect others
- **Flexibility**: Easy to swap implementations (e.g., replace the in-memory store with a real database by only changing the DAO layer)

#### Request Flow Example

```
HTTP Request
    │
    ▼
Blueprint (routes.py)           →  Defines endpoint URL
    │
    ▼
Controller (note_controller.py) →  Handles request/response
    │
    ▼
Service (note_service.py)       →  Applies business rules
    │
    ▼
DAO (note_dao.py)               →  Executes data operation
    │
    ▼
In-Memory Store (_store list)   →  Stores/retrieves data
```

### Design Patterns

#### 1. Factory Pattern

**Purpose**: Creates objects without specifying the exact class to create. Useful for creating instances with different configurations.

**Location**: `app.py`

```python
ALLOWED_CONFIGS = {"development", "production", "testing"}

def create_app(config_name: str = "development") -> Flask:
    if config_name not in ALLOWED_CONFIGS:
        raise ValueError(f"Invalid config_name: {config_name!r}.")

    app = Flask(__name__)

    config_module = importlib.import_module(f"src.configs.{config_name}_config")
    app.config.from_object(config_module.__dict__[f"{config_name.capitalize()}Config"])

    register_routes(app)

    if app.config.get("SEED_DEFAULTS", False):
        add_default_notes()

    return app


# Usage
app = create_app("development")  # Development environment
app = create_app("testing")      # Testing environment
app = create_app("production")   # Production environment
```

#### 2. Repository Pattern (DAO)

**Purpose**: Abstracts data access logic, providing a clean API for data operations. The business layer doesn't know how data is stored.

**Location**: `src/data_access/note_dao.py`

```python
_store: list[dict[str, Any]] = []

class NoteDAO:
    @staticmethod
    def insert_one(note: dict[str, Any]) -> dict[str, Any]:
        entry = {"_id": str(uuid.uuid4()), "created_at": ..., **note}
        _store.append(entry)
        return entry

    @staticmethod
    def find() -> list[dict[str, Any]]:
        return list(_store)

    @staticmethod
    def find_one_by_id(_id: str) -> dict[str, Any] | None:
        return next((n for n in _store if n["_id"] == _id), None)

    @staticmethod
    def delete_one_by_id(_id: str) -> bool:
        ...
```

**Benefit**: If you switch from in-memory to a real database, only the DAO layer changes.

#### 3. Service Layer Pattern

**Purpose**: Encapsulates business logic in a dedicated layer. Controllers stay thin, and business rules are centralized.

**Location**: `src/services/note_service.py`

```python
class NoteService:
    @staticmethod
    def add_note(note: NoteModel) -> dict[str, Any]:
        # Business rule: Check for duplicates
        existing = NoteDAO.find_one_by_name(note.name)
        if existing:
            raise ConflictAPIError(
                code=CODE_ALREADY_EXISTS_NOTE,
                message=MESSAGE_ALREADY_EXISTS_NOTE,
            )
        return NoteDAO.insert_one(note.model_dump())

    @staticmethod
    def delete_note_by_id(_id: str) -> bool:
        # Business rule: Verify existence before deletion
        existing = NoteDAO.find_one_by_id(_id)
        if not existing:
            raise NotFoundAPIError(
                code=CODE_NOT_FOUND_NOTE,
                message=MESSAGE_NOT_FOUND_NOTE,
            )
        return NoteDAO.delete_one_by_id(_id)
```

**Benefit**: Business rules are in one place, not scattered across controllers.

#### 4. Decorator Pattern

**Purpose**: Adds behavior to functions without modifying them. Wraps functions to extend functionality.

**Location**: `src/utils/exceptions_decorator.py`

```python
def exceptions_decorator(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return fn(*args, **kwargs)

        except ValidationError as e:
            raise ValidationAPIError(
                code=CODE_ERROR_PYDANTIC,
                message=MESSAGE_ERROR_PYDANTIC,
                payload={"details": e.errors()},
            ) from e

    return wrapper
```

**Usage in Controller**:

```python
@exceptions_decorator
def alive() -> ResponseReturnValue:
    response = {"message": "I am Alive!"}
    return jsonify(response), 200


@exceptions_decorator
def create_note() -> ResponseReturnValue:
    body = request.get_json() or {}
    note = NoteModel(**body)
    data = NoteService.add_note(note)
    return jsonify({"code": CODE_SUCCESS_ADD_NOTE, "message": MESSAGE_SUCCESS_ADD_NOTE, "data": data}), 201
```

**Benefit**: No need to repeat try/catch blocks in every controller.

#### 5. Template Method Pattern

**Purpose**: Defines a base structure that subclasses can customize by overriding specific parts.

**Location**: `src/configs/`

```python
# src/configs/default_config.py - Base template
class DefaultConfig:
    TZ = os.getenv("TZ", "America/Argentina/Buenos_Aires")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))
    DEBUG = False
    TESTING = False
    SEED_DEFAULTS = False


# src/configs/development_config.py - Customizes for development
class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    SEED_DEFAULTS = True


# src/configs/testing_config.py - Customizes for testing
class TestingConfig(DefaultConfig):
    TESTING = True
    DEBUG = True


# src/configs/production_config.py - Customizes for production
class ProductionConfig(DefaultConfig):
    DEBUG = False
    TESTING = False
```

**Benefit**: Common configuration in one place; environments only override what's different.

## API Endpoints

To see the layers above in action, here are the endpoints exposed by the example resource. The `note` resource ships with two seeded entries on startup and demonstrates the complete CRUD flow through the layered architecture.

The note resource endpoints are prefixed with `/api/v1/notes`. The health endpoint is prefixed with `/api/v1/health`.

### Application Health

| Method | Path             | Description                             |
| ------ | ---------------- | --------------------------------------- |
| `GET`  | `/api/v1/health` | Liveness check — confirms the app is up |

**Response 200 — `/api/v1/health`:**

```json
{ "code": "SUCCESS_HEALTH", "message": "The application is healthy." }
```

### Note Resource Health

| Method | Path     | Description                               |
| ------ | -------- | ----------------------------------------- |
| `GET`  | `/alive` | Returns API status and blueprint metadata |

**Response 200:**

```json
{
  "message": "I am Alive!",
  "version_bp": "1.0.0",
  "author": "Diego Libonati",
  "name_bp": "Note"
}
```

### Notes

| Method   | Path    | Description               |
| -------- | ------- | ------------------------- |
| `POST`   | `/`     | Create a new note         |
| `GET`    | `/`     | Retrieve all notes        |
| `DELETE` | `/<id>` | Delete a note by its UUID |

#### POST `/`

**Request body:**

```json
{ "name": "my note" }
```

**Response 201:**

```json
{
  "code": "SUCCESS_ADD_NOTE",
  "message": "The note was successfully added.",
  "data": {
    "_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2026-05-02T12:00:00+00:00",
    "name": "my note"
  }
}
```

**Response 409** — note with same name already exists:

```json
{ "code": "ALREADY_EXISTS_NOTE", "message": "Note already exists." }
```

**Response 400** — validation error (e.g., empty name):

```json
{
  "code": "ERROR_PYDANTIC",
  "message": "Pydantic error.",
  "payload": { "details": [...] }
}
```

#### GET `/`

**Response 200:**

```json
{
  "code": "SUCCESS_GET_NOTES",
  "message": "Notes retrieved successfully.",
  "data": [
    { "_id": "...", "created_at": "...", "name": "hi" },
    { "_id": "...", "created_at": "...", "name": "im Die" }
  ]
}
```

#### DELETE `/<id>`

**Response 200:**

```json
{
  "code": "SUCCESS_DELETE_NOTE",
  "message": "The note was successfully deleted."
}
```

**Response 404** — ID not found:

```json
{ "code": "NOT_FOUND_NOTE", "message": "No note found." }
```

> **Note on persistence:** The in-memory store resets every time the app restarts. To persist data, replace the `_store` list in `src/data_access/note_dao.py` with a real database client — the service and controller layers require zero changes.

## Testing

Once the API is up, you can verify it end-to-end with the test suite.

1. Activate the virtual environment (see [Local Virtual Environment](#local-virtual-environment))
2. Execute: `pytest --log-cli-level=INFO`

## Security Audit

Beyond functional tests, scan production dependencies for known vulnerabilities using **pip-audit**.

1. Activate the virtual environment (see [Local Virtual Environment](#local-virtual-environment))
2. Execute: `pip-audit --skip-editable`

## Build

When tests are green and the dependency audit is clean, build the Docker image you intend to ship.

### Development image

```
docker-compose -f dev.docker-compose.yml build --no-cache
```

### Production image

```
docker-compose -f prod.docker-compose.yml build --no-cache
```

NOTE: You must stand in the folder containing the corresponding compose file. Install **Docker Desktop** if you are on Windows.

## Continuous Integration

The repository ships with a **GitHub Actions** pipeline defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml). It runs automatically on every `push` and `pull_request` targeting the `main` branch.

### Pipeline overview

```
                      ┌─── PR or push to main ───┐
                      ▼                          ▼
┌──────────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│   lint-and-audit     │─▶│       test       │─▶│     docker-build     │
│ ruff · mypy · audit  │  │      pytest      │  │ dev image · prod img │
└──────────────────────┘  └──────────────────┘  └──────────────────────┘
```

### Validation jobs (run on every PR and push)

1. **`lint-and-audit`** — `ruff check .`, `ruff format --check .`, `mypy --config-file=pyproject.toml .`, `pip-audit --skip-editable`.
2. **`test`** — installs the `test` extra and runs `python -m pytest --tb=short`.
3. **`docker-build`** — matrix job that runs Docker Buildx against `Dockerfile.development` (tagged `app:dev`) and `Dockerfile.production` (tagged `app:prod`). Images are built but not pushed — this is a smoke test that both Dockerfiles still build from a clean context.

Each job runs sequentially: `lint-and-audit` → `test` → `docker-build`. If a stage fails, the following stages are skipped.

### Where the build outputs live

| Output                          | Location                          |
| ------------------------------- | --------------------------------- |
| Validation logs (lint, tests)   | **Actions** tab on GitHub         |
| Docker images (dev & prod)      | Ephemeral, inside the runner      |

> **Note:** The Docker images built in CI are not pushed to any registry. They exist only to verify the Dockerfiles still build. If you need to publish images (e.g., to GHCR, Docker Hub, ECR), extend `docker-build` with a login step and `push: true`.

### Running the same checks locally

```bash
# lint-and-audit
ruff check .
ruff format --check .
mypy --config-file=pyproject.toml .
pip-audit --skip-editable

# test
python -m pytest --tb=short

# docker-build (development image)
docker build -f Dockerfile.development -t app:dev .

# docker-build (production image)
docker build -f Dockerfile.production -t app:prod .
```

## Production

With the image built, follow this checklist to bring the API up in production. This section does not duplicate prior steps — it links to them.

1. Set your production environment variables in `.env` (see [Env Keys](#env-keys))
2. Run the test suite (see [Testing](#testing))
3. Run the dependency audit (see [Security Audit](#security-audit))
4. Build the production image (see [Build → Production image](#production-image))
5. Start the container: `docker-compose -f prod.docker-compose.yml up -d`

### What's different from development

|                | Development      | Production             |
| -------------- | ---------------- | ---------------------- |
| Server         | Flask dev server | Gunicorn (`wsgi.py`)   |
| Debug mode     | `True`           | `False`                |
| Docker image   | Single-stage slim image | Multi-stage slim image |
| Container user | root             | `appuser` (non-root)   |

### Gunicorn

The production server is configured in `src/configs/gunicorn_config.py`:

- **Workers**: `cpu_count * 2 + 1` (auto-scaled to the host machine)
- **Threads**: `2` per worker
- **Timeout**: `120s` (request), `30s` (graceful shutdown)
- **Logs**: stdout/stderr (compatible with Docker log drivers)

### Security considerations

- The production Dockerfile runs the app as a non-root user (`appuser`) — do not override this.
- Re-run the [Security Audit](#security-audit) before every deploy, not only on the first one.

## Known Issues

None at the moment.

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/python-flask-api-boilerplate`](https://www.diegolibonati.com.ar/#/project/python-flask-api-boilerplate)
