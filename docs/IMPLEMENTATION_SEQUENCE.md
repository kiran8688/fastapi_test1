# Implementation Sequence Guide

Building a project of this scale from scratch requires a structured, step-by-step approach. Here is the exact sequence to follow to develop this kind of project in the future.

---

### Step 1: Project Setup and Environment
1. **Initialize a Python environment**:
   - Create a virtual environment (`python -m venv .venv`).
   - Create a `requirements.txt` file and install essential packages: `fastapi`, `uvicorn`.
2. **Create the Project Skeleton**:
   - Create the `app/` package folder.
   - Create an `app/main.py` file with a minimal FastAPI instance returning `{"Hello": "World"}`.
   - Run the server `uvicorn app.main:app --reload` to verify the setup.

---

### Step 2: Database Setup & ORM Integration
1. **Setup PostgreSQL**:
   - Install PostgreSQL locally or run it via Docker.
   - Create a database (e.g., `Fastapi_test1`).
2. **Setup SQLAlchemy**:
   - Add `sqlalchemy` and `psycopg2-binary` (or `psycopg`) to `requirements.txt`.
   - Create `app/database.py`. Configure the `create_engine()`, `SessionLocal`, and declarative `Base`.
   - Create a `get_db()` dependency to manage database sessions.
3. **Environment Variables Config**:
   - Add `pydantic-settings` to requirements.
   - Create `app/config.py` to securely store database credentials, parsing variables from a `.env` file. Update `database.py` to use these settings.

---

### Step 3: Database Models & Database Migrations (Alembic)
1. **Create Models**:
   - Create `app/models.py`.
   - Define your basic SQLAlchemy models (e.g., `User` and `Post` classes) inheriting from `Base`.
2. **Setup Alembic**:
   - Add `alembic` to `requirements.txt` and run `alembic init alembic`.
   - Configure `alembic.ini` (Point it to your database URL).
   - In `alembic/env.py`, import your Base and target the `Base.metadata`.
3. **Run Initial Migrations**:
   - Create the first migration script: `alembic revision --autogenerate -m "initial tables"`.
   - Apply the tables: `alembic upgrade head`.

---

### Step 4: Data Validation with Pydantic (Schemas)
1. **Define Request/Response Schemas**:
   - Create `app/schemas.py`.
   - Write Pydantic models for incoming requests (e.g., `AddPost`, `AddUser`).
   - Write Pydantic models for outgoing responses (e.g., `PostOut`, `UserOut`) using `model_config = ConfigDict(from_attributes=True)` to convert SQLAlchemy objects to JSON.

---

### Step 5: Core Domain Logic & Routing (CRUD Operations)
Instead of keeping all routes in `main.py`, modularize them.

1. **User Router (`app/routers/user.py`)**:
   - Create endpoints to register new users and retrieve users by ID.
   - Add password hashing logic (e.g., using `passlib` in `app/utils.py` to hash passwords before saving them).
2. **Post Router (`app/routers/post.py`)**:
   - Create endpoints for `GET`, `POST`, `PUT`, `DELETE` operations for posts.
   - Use `Depends(get_db)` to interact with the database.
   - Link these routers back to `app/main.py` using `app.include_router()`.

---

### Step 6: Authentication & JWT Tokens
1. **Login Endpoint (`app/routers/auth.py`)**:
   - Create a login route.
   - Verify the user's email and hashed password.
2. **JWT Setup (`app/oauth2.py`)**:
   - Implement `create_access_token()` using `PyJWT`.
   - Create a `get_current_user` dependency. This function extracts the JWT token from the HTTP headers, decodes it, and fetches the matching user.
3. **Secure the Architecture**:
   - Inject the `current_user: int = Depends(oauth2.get_current_user)` dependency into protected routes (like creating a post or voting).
4. **Relational Links**:
   - Enhance the `Post` model by adding a foreign key `owner_id` that maps to the `User.id`. This binds posts securely to their creators.

---

### Step 7: Complex Operations (The Voting System)
1. **Vote Model**:
   - Add a `Vote` table in `models.py` (composite primary key of `user_id` and `post_id`). Provide an Alembic migration.
2. **Vote Router (`app/routers/vote.py`)**:
   - Build an endpoint allowing authenticated users to insert/remove a record from the Vote table.
3. **Join Queries**:
   - Update the `GET /posts` endpoint using complex SQLAlchemy `join()` queries to aggregate total votes for each post (using `func.count()`).

---

### Step 8: Testing, CI/CD, and Dockerization
1. **Automated Testing**:
   - Add a `tests/` directory. Use `pytest`.
   - Map a test database fixture (overriding `get_db`). Write tests asserting that your CRUD operations behave gracefully on edge cases.
2. **Dockerization**:
   - Write a `Dockerfile` for the application.
   - Write `docker-compose-dev.yaml` orchestrating PostgreSQL and the FastAPI web container together.

### Summary
1. Core HTTP Server (FastAPI)
2. Database connection & ORM Setup (SQLAlchemy)
3. DB schema migrations (Alembic)
4. Shapes & Validations (Pydantic)
5. Modulized Routers 
6. Authentication & Safety (JWT, Hashing)
7. Advanced business queries (Voting, JOINs)
8. Testing & Docker.
