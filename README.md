# Python Flask Api Boilerplate

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

> **Want a MongoDB version?** Check out [`python-flask-mongo-api-boilerplate`](https://github.com/DiegoLibonati/python-flask-mongo-api-boilerplate) — the same boilerplate adapted to work with MongoDB and PyMongo.

## Getting Started for Development

1. Clone the repository
2. Go to the repository folder and execute: `docker-compose -f dev.docker-compose.yml build --no-cache` in the terminal
3. Once built, you must execute the command: `docker-compose -f dev.docker-compose.yml up --force-recreate` in the terminal

NOTE: You have to be standing in the folder containing the: `dev.docker-compose.yml` and you need to install `Docker Desktop` if you are in Windows.

### Pre-Commit for Development

NOTE: Install **pre-commit** inside repository folder.

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

### Create a Virtual Env for Pre-Commit and Tests (And other things)

1. Join to the correct path of the clone
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute in Linux/Mac: `source venv/bin/activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.dev.txt`
7. Execute: `pip install -r requirements.test.txt`
8. Execute all the commands you want

## Getting Started for Production

1. Clone the repository
2. Set your production environment variables in `.env` (see **Env Keys** section)
3. Go to the repository folder and execute: `docker-compose -f prod.docker-compose.yml build --no-cache` in the terminal
4. Once built, execute: `docker-compose -f prod.docker-compose.yml up -d` in the terminal

### What's different from development

| | Development | Production |
|---|---|---|
| Server | Flask dev server | Gunicorn (`wsgi.py`) |
| Debug mode | `True` | `False` |
| Docker image | Full build | Multi-stage slim image |
| Container user | root | `appuser` (non-root) |

### Gunicorn

The production server is configured in `src/configs/gunicorn_config.py`:

- **Workers**: `cpu_count * 2 + 1` (auto-scaled to the host machine)
- **Threads**: `2` per worker
- **Timeout**: `120s` (request), `30s` (graceful shutdown)
- **Logs**: stdout/stderr (compatible with Docker log drivers)

### Security considerations before deploying

- Run `pip-audit -r requirements.txt` to check for known vulnerabilities in production dependencies
- The production Dockerfile runs the app as a non-root user (`appuser`) — do not override this

## Description

**Python Flask Api Boilerplate** is a production-ready starting point for building REST APIs with **Flask**, designed to eliminate the repetitive setup and architectural decisions that come with every new backend project.

**What it is:** A starting point — not a framework — for developers who want to spin up a Flask API without rebuilding the same infrastructure from scratch each time. Every layer, pattern, and tooling choice is already wired together and working.

**The problem it solves:** Starting a Flask API from zero means making the same decisions repeatedly: how to structure layers, how to handle errors globally, how to validate input, how to configure environments, how to set up Docker, linting, tests, and security audits. This boilerplate makes all those decisions once, so you can focus on building the actual product.

**The example resource:** The boilerplate ships with a fully functional `note` resource that manages a simple list of named entries stored **in memory**. It demonstrates every layer of the architecture (Blueprint → Controller → Service → DAO) without requiring any external database. When you're ready to connect a real database, you only need to replace the DAO layer — everything else stays the same.

**What it includes:**
- **Layered architecture** enforced by convention: Blueprint → Controller → Service → DAO → In-Memory Store. Each layer has a single responsibility and only talks to the one directly below it.
- **Pydantic v2** for request validation and data serialization, with a custom `exceptions_handler` decorator that automatically converts `ValidationError` into structured JSON API responses — no try/catch boilerplate in controllers.
- **Custom exception hierarchy** (`ValidationAPIError`, `NotFoundAPIError`, `ConflictAPIError`, `InternalAPIError`) that produces consistent error responses across the entire API.
- **Environment-based configuration** using a `DefaultConfig` base class extended by `DevelopmentConfig`, `TestingConfig`, and `ProductionConfig`, loaded dynamically by the app factory.
- **Docker** setup for development and production, with a multi-stage Dockerfile for slim production images.
- **Gunicorn** as the production WSGI server, configured via `gunicorn_config.py`.
- **Ruff** for fast linting and formatting, enforced automatically via **pre-commit** hooks on every commit.
- **pip-audit** integration for scanning production dependencies against known vulnerability databases.
- **pytest** configured and organized to mirror the `src/` structure.
- **Startup initialization** layer (`src/startup/`) for seeding default data when the app boots.

**How to use it:** Clone the repository, bring up the Docker environment, and replace the `note` resource (blueprint, controller, service, DAO, model, constants) with your own domain logic. The architecture, tooling, and error handling are already in place — you only write what's unique to your application.

## API Endpoints

The boilerplate ships with a fully functional `note` resource that manages named entries stored **in memory**. It seeds two default entries on startup and demonstrates the complete CRUD flow through the layered architecture.

All endpoints are prefixed with `/api/v1/notes`.

### Health

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/alive` | Returns API status and blueprint metadata |

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

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/` | Create a new note |
| `GET` | `/` | Retrieve all notes |
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

## Technologies used

1. Python -> Flask
2. Docker
3. Gunicorn

## Libraries used

#### Requirements.txt

```
flask==3.1.3
pydantic==2.11.9
gunicorn==23.0.0
```

#### Requirements.dev.txt

```
pre-commit==4.3.0
pip-audit==2.7.3
ruff==0.11.12
```

#### Requirements.test.txt

```
pytest==8.4.2
pytest-env==1.1.5
pytest-cov==4.1.0
pytest-timeout==2.3.1
pytest-xdist==3.5.0
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/python-flask-api-boilerplate`](https://www.diegolibonati.com.ar/#/project/python-flask-api-boilerplate)

## Testing

1. Join to the correct path of the clone
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute: `pip install -r requirements.txt`
5. Execute: `pip install -r requirements.test.txt`
6. Execute: `pytest --log-cli-level=INFO`

## Security Audit

You can check your dependencies for known vulnerabilities using **pip-audit**.

1. Go to the repository folder
2. Activate your virtual environment
3. Execute: `pip install -r requirements.dev.txt`
4. Execute: `pip-audit -r requirements.txt`

## Env Keys

1. `TZ`: Refers to the timezone setting for the container.
2. `HOST`: Refers to the network interface where the backend API listens (e.g., 0.0.0.0 to allow external connections).
3. `PORT`: Refers to the port on which the backend API is exposed.

```ts
TZ=America/Argentina/Buenos_Aires

HOST=0.0.0.0
PORT=5050
```

## Project Structure

```
python-flask-api-boilerplate/
├── src/
│   ├── blueprints/
│   │   ├── routes.py
│   │   └── v1/
│   │       └── note_bp.py
│   ├── configs/
│   │   ├── default_config.py
│   │   ├── development_config.py
│   │   ├── production_config.py
│   │   ├── testing_config.py
│   │   ├── gunicorn_config.py
│   │   └── logger_config.py
│   ├── controllers/
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
│       ├── exceptions_handler.py
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
├── .env
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
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
10. `utils` -> Contains **shared utilities** including custom exceptions, error handling decorators, and helper functions.
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
def create_app(config_name="development") -> Flask:
    app = Flask(__name__)

    config_module = importlib.import_module(f"src.configs.{config_name}_config")
    app.config.from_object(config_module.__dict__[f"{config_name.capitalize()}Config"])

    register_routes(app)
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

**Location**: `src/utils/exceptions_handler.py`

```python
def exceptions_handler(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return fn(*args, **kwargs)

        except ValidationError as e:
            raise ValidationAPIError(
                code=CODE_ERROR_PYDANTIC,
                message=MESSAGE_ERROR_PYDANTIC,
                payload={"details": e.errors()},
            )

    return wrapper
```

**Usage in Controller**:

```python
@exceptions_handler
def alive() -> Response:
    response = {"message": "I am Alive!"}
    return jsonify(response), 200


@exceptions_handler
def create_note() -> Response:
    # If ValidationError occurs, it's automatically caught and
    # converted to a structured API error response
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
    PORT = os.getenv("PORT", 5000)
    DEBUG = False
    TESTING = False


# src/configs/development_config.py - Customizes for development
class DevelopmentConfig(DefaultConfig):
    DEBUG = True


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

## Known Issues

None at the moment.
