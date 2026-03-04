# 🚀 FastAPI Backend Master Guide | Developed by [Kiran](https://github.com/kiran8688)

Welcome to your project's central brain! This document is designed to be your ultimate reference point. It breaks down exactly how this application works beneath the surface, how all the individual files connect to form a cohesive system, the strategic sequence to follow when building something like this from scratch, and how to successfully run and debug it.

Whether you are returning to this codebase after weeks away or preparing to build a larger, more complex version, this guide will serve as your architectural blueprint.

## 🌟 1. Project Walkthrough (What exactly is this?)

At its core, this project is a fully functional **RESTful API** tailored for a Blog, Forum, or Social Media backend platform. It acts as the invisible engine that a frontend website or mobile app would talk to.

It handles the following core business logic:

1. **User Identity & Security**: Users can register accounts and log in. Instead of traditional sessions, it issues **JWT (JSON Web Tokens)** for stateless, scalable authentication.
2. **Content Management (CRUD)**: Authorized users can **C**reate, **R**ead, **U**pdate, and **D**elete posts. The system ensures users can only edit or delete their *own* content.
3. **Complex Relationships (Voting/Liking)**: Users can upvote or downvote posts. This demonstrates a many-to-many relational database concept, ensuring a user can only vote on a specific post once.

### Why this Tech Stack?

Every tool in this project was chosen for a specific, modern, industry-standard reason:

* **FastAPI**: Selected for its incredible speed, automatic data validation, and built-in interactive documentation (Swagger UI).
* **PostgreSQL**: A robust, enterprise-grade relational database perfect for handling strict relationships (like Users -> Posts -> Votes).
* **SQLAlchemy (ORM)**: Allows you to write Python code instead of raw SQL strings. It automatically translates your Python classes into database tables, significantly reducing the risk of SQL injection attacks.
* **Alembic**: The "time machine" for your database. As your project grows and you add new columns to your tables, Alembic safely migrates the database without losing existing data.
* **Docker**: Solves the classic "it works on my machine" problem by bundling the app, the database, and the operating system into portable containers.

## 🏗️ 2. The Development Mindmap (Sequence to Implement)

When tackling a project of this scale, the biggest mistake is trying to write everything at once. Professional development is about building isolated, testable layers. If you need to build this exact project (or a larger one) again, follow this exact chronological sequence:

 1. **Environment Setup & Groundwork:** Create the folder, set up a virtual environment (`venv`), and install core packages like `fastapi` and `uvicorn`. Isolates your project's dependencies.
 2. **The "Hello World" Prototype:** Create `main.py`, write a single `@app.get("/")` route, and start the server. Validates that your web server framework is working.
 3. **Pydantic Schemas (`schemas.py`):** Define what the data should look like when a user sends it and returning it. FastAPI uses these to automatically validate incoming JSON.
 4. **Database Connection (`database.py` & `config.py`):** Set up SQLAlchemy engine and sessions. Use `pydantic-settings` to load environment variables securely.
 5. **Database Models (`models.py`):** Create the Python classes (`User`, `Post`, `Vote`) that map to SQL tables. strict data structure for Database.
 6. **Basic CRUD Routers (`routers/post.py` & `routers/user.py`):** Move routes out of `main.py` into modular files using `APIRouter`.
 7. **Security Setup (`utils.py`):** Implement password hashing (e.g., Argon2/Bcrypt) to never store plain-text passwords.
 8. **Authentication & Authorization (`oauth2.py` & `routers/auth.py`):** Create the `/login` endpoint to verify passwords and generate JWT tokens. Create the `get_current_user` dependency.
 9. **Advanced Features & Relationships (`routers/vote.py`):** Implement the voting system, linking the `User` and the `Post` via a composite primary key.
10. **Database Migrations (`alembic/`):** Initialize Alembic to track changes to `models.py` and safely upgrade schemas in production.
11. **Containerization & Deployment (`Dockerfile` & `docker-compose`):** Write instructions for Docker to build your environment.

## 📂 3. Folder Structure Map

Here is how your project is strictly organized. Understanding this layout is crucial for navigating large codebases:

```text
fastapi_test1/
│
├── app/                        # Main Application Package
│   ├── __init__.py             # Makes 'app' a python module
│   ├── main.py                 # 🚀 Entry point of the application (FastAPI instance, CORS, Router registrations)
│   ├── config.py               # Configuration Manager (Environment variables, Pydantic type-checking)
│   ├── database.py             # Database Gateway (PostgreSQL connection setup & get_db session dependency)
│   ├── models.py               # Database Blueprint (SQLAlchemy tables: users, posts, votes)
│   ├── schemas.py              # API Gatekeeper (Pydantic models for request/response validation)
│   ├── utils.py                # Toolbelt (Password hashing and verification)
│   ├── oauth2.py               # Security Officer (JWT Token creation and verification logic)
│   └── routers/                # API Endpoints grouped by feature
│       ├── auth.py             # Handles user login and token generation
│       ├── post.py             # Handles all logic relating to the blog posts
│       ├── user.py             # Handles account registration and fetching user profiles
│       └── vote.py             # Handles the logic for liking/unliking posts
│
├── tests/                      # Quality Assurance (pytest scripts)
│   ├── __init__.py
│   └── test_users.py           # Unit tests for user-related features
│
├── alembic/                    # Database Migration Tool (alembic scripts)
│   ├── versions/               # Contains migration scripts
│   └── env.py                  # Alembic environment setup
│
├── .env                        # 🤫 Environment variables (DB credentials, secret key)
├── .gitignore                  # Files to be ignored by Git
├── alembic.ini                 # Alembic configuration file (Points to database URL)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Instructions to build the Docker image
├── docker-compose-dev.yaml     # Orchestrating both DB and API (Development)
└── docker-compose-prod.yaml    # Production orchestration
```

## � 4. Code Flow Map (The Assembly Line)

When a user makes an API request, data travels through your files in a highly controlled, specific order based on **Dependency Injection**. Let's trace a `POST /posts/` request:

1. **The Arrival (`main.py`)**: The HTTP request arrives. `main.py` intercepts it, reads the `/posts/` URL, and delegates it to the `post.py` router.
2. **Security Check (`oauth2.py`)**: Before the route looks at the data, `Depends(oauth2.get_current_user)` intercepts headers, extracts/decodes the JWT token, finds the user, and hands the User object to the route (or throws 401 Unauthorized).
3. **Data Validation (`schemas.py`)**: The router forces incoming JSON through the `AddPost` schema. Pydantic validates types and throws a 422 if invalid.
4. **Database Session (`database.py`)**: `Depends(get_db)` opens a fresh tunnel to PostgreSQL for this request.
5. **Data Transformation (`models.py`)**: The dictionary is mapped into the `Post` SQLAlchemy model, adding the `owner_id`.
6. **Execution**: The database session commits the new record to PostgreSQL.
7. **Response Formatting (`schemas.py`)**: The fresh record is pushed through the `PostOut` schema, stripping sensitive data, and shipped back as JSON (201 Created).

## 📊 5. Architecture Diagrams

For deeper insights into the diagrams, check out the `docs/` folder!
* **Sequence Diagram**: Visualizes the timeline of file interactions described in the "Code Flow Map". (`docs\mermaid-files-diagram.png`)
*This diagram visually maps out the timeline and interactions described in the "Code Flow Map" above.*

![Sequence Diagram](https://github.com/kiran8688/fastapi_test1/blob/main/docs/mermaid-files-diagram.png)
* **Authentication Flow**: Mechanism mapping identity verification over `/login` endpoints. (`docs\JWT-Login_Authentication_Flow_Diagram.png`)
*This diagram illustrates the step-by-step process of user authentication, from token verification to user extraction.*

![Authentication Flow](https://github.com/kiran8688/fastapi_test1/blob/main/docs/JWT-Login_Authentication_Flow_Diagram.png)
* **CRUD Flow**: Breakdown of data retrieval strategies (e.g. Get Post by ID). (`docs\FastAPI-Get_Post_by_ID-Flow_Diagram.png`)
*This diagram illustrates the step-by-step process of user authentication, from token verification to user extraction.*

![CRUD Flow](https://github.com/kiran8688/fastapi_test1/blob/main/docs/FastAPI-Get_Post_by_ID-Flow_Diagram.png)

## 💻 6. Installation, Run, & Debug Instructions

### Prerequisites

* **Python 3.8+** installed.
* **PostgreSQL** installed locally OR **Docker Desktop** installed and running.

### Option 1: Running via Docker (Highly Recommended)

This method handles all complex database setup automatically.

1. Start **Docker Desktop**.
2. **Setup Environment Variables**: Create a `.env` file in the root directory:
   ```env
   DATABASE_HOSTNAME=fastapi1_postgres
   DATABASE_PORT=5432
   DATABASE_PASSWORD=12345678
   DATABASE_NAME=Fastapi_test1
   DATABASE_USERNAME=postgres
   SECRET_KEY=generate_a_long_random_string_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
3. **Boot up & View Logs:**
   ```bash
   docker-compose -f docker-compose-dev.yaml up -d
   docker-compose -f docker-compose-dev.yaml logs -f api
   ```
4. **Shut Down:** `docker-compose -f docker-compose-dev.yaml down`

### Option 2: Running Locally (Manual Setup)

Use this if you want to run Python directly for easier step-through debugging.

1. **Activate Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Setup Database Manually:** Create a database named `Fastapi_test1` (via pgAdmin/psql). Update your `.env` to set `DATABASE_HOSTNAME=localhost`.
3. **Run Migrations:** Initialize tables via Alembic:
   ```bash
   alembic upgrade head
   ```
4. **Start the Development Server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   *Visit `http://127.0.0.1:8000/docs` to test endpoints directly in your browser using interactive Swagger UI.*

### 🛠️ Common Alembic Migration Commands

Database schemas change over time. When you add or modify a column in `app/models.py`, you **must** generate a migration.

1. **Generate script:** `alembic revision --autogenerate -m "describe_changes"`
2. **Apply changes:** `alembic upgrade head`
3. **Rollback mistake:** `alembic downgrade -1`

## 🎯 7. Use Cases

- **Frontend App Integration**: Can be consumed by React, Vue, or Angular to create a full-stack social networking site.
- **Mobile App**: Backend for an Android/iOS application.
- **Learning**: Acts as a perfect reference architecture for building clean, scalable APIs in Python.

---
### 🏆 Developed by [Kiran](https://github.com/kiran8688)
*Trademark © 2024 Kiran8688*

