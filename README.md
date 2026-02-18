
https://github.com/user-attachments/assets/6c67ccc5-c87a-419c-84eb-7fdc3a6b1296
# 🏦 Banking API

Author : Shivani Sharma

A **FastAPI-based internal banking API** that simulates essential financial operations such as customer onboarding, account management, balance checks, and money transfers.

This project is implemented as a **production-oriented prototype**, following clean architecture principles, Python best practices, **enforced Role-Based Access Control (RBAC)**, and a clearly documented path to production.

---

## 🎥 Demo Videos

A short walkthrough demonstrating authentication, RBAC enforcement, and core API flows:

https://drive.google.com/drive/folders/1uyFHK2RxYxUKwkWGxF9nhQgUuan_RhxP?usp=drive_link

## 📌 Key Highlights

- JWT-based authentication
- **Role-Based Access Control (RBAC) enforced**
- Atomic money transfers
- Clean, maintainable architecture
- Dockerized setup (runs out of the box)
- Docker Compose orchestration
- GitLab CI/CD integration
- Clear production-readiness roadmap

---

## ✨ Features

- Customer registration & login
- JWT authentication
- Role-based authorization:
  - **Admin** – full access
  - **Employee** – manage accounts & transfers
  - **Customer** – access own accounts only
- Account creation with initial deposits
- Balance retrieval
- Secure money transfers
- Transfer history per account
- Automatic database initialization
- Default admin & customer seeding
- Interactive Swagger (OpenAPI) documentation

---

## 🛠 Tech Stack

| Layer | Technology |
|------|------------|
| Language | Python 3.9 |
| API Framework | FastAPI |
| ASGI Server | Uvicorn |
| ORM | SQLAlchemy |
| Database | SQLite (development only) |
| Authentication | JWT |
| Authorization | RBAC |
| Containers | Docker |
| Orchestration | Docker Compose |
| CI/CD | GitLab CI/CD |
| Testing | Pytest |

---

## 🚀 Getting Started (Development)

Prerequisites

- Docker

- Docker Compose

1. Clone the Repository
git clone <repository-url>
cd <project-directory>

2. Build & Run the Application
docker compose up --build

3. API Access

The API will be available at:

http://localhost:8000/docs

4. Stop the Application
docker compose down

----

## 🔑 Authentication & Authorization

- Authentication via JWT

- Authorization enforced using RBAC

- All protected endpoints validate:

- Token validity

- User role

- Resource ownership

Example request header
Authorization: Bearer <access_token>

---

## 🧩 System Design (High Level)

The application follows a layered architecture for clarity and maintainability:

Client --> API Routes (FastAPI) --> Service Layer (Business Logic) --> Data Access Layer (SQLAlchemy ORM) --> Database (SQLite)


Business rules are handled in the service layer, while routes remain thin and focused on request/response handling.

| Model    | Responsibility                           |
| -------- | ---------------------------------------- |
| Customer | System users (admin, employee, customer) |
| Account  | Account ownership & balance              |
| Transfer | Atomic money movement                    |
| Role     | RBAC permissions                         |
| AuditLog | Sensitive operation tracking             |

---

## 🧪 Running Tests
pytest -q


Tests cover authentication, RBAC enforcement, account operations, and transfer edge cases.

## 📚 API Documentation

Interactive API documentation is available via Swagger UI:

http://localhost:8000/docs

## 🧱 CI/CD Pipeline

**GitLab CI/CD stages:**

- Run automated tests

- Build Docker image

- Push image to GitLab Container Registry

- Deploy to development server using Docker Compose

The application can be installed and tested out of the box by reviewers.

**Alternative:**
1. git clone <repo-url>
2. cd project-name
3. python -m venv venv
4. source venv/bin/activate   ( mac/linux) or venv\Scripts\activate (windows)
5. pip install -r requirements.txt
6. uvicorn app.main:app --reload
  
## 📐 Technology Choices & Rationale
- FastAPI was chosen for its strong typing, automatic validation, and clean structure, enabling a correct and maintainable API design.

- SQLite was used to ensure zero-setup execution for reviewers while still demonstrating proper data modeling and transactional logic.

- Swagger (OpenAPI) provides self-documenting, interactive API exploration, allowing reviewers to validate functionality without external tools.

- The stack minimizes setup friction while maintaining a clear and realistic path to production.

## Frontend Integration Using React.js

- React.js can be used to build a single-page frontend that consumes the FastAPI REST APIs.

- JWT-based authentication enables secure communication and role-based UI rendering for Admin, Employee, and Customer roles.

- The frontend handles presentation and user interaction, while all business logic and access control remain enforced on the backend.

- This approach cleanly separates concerns and allows the system to scale from prototype to production.

## 🏁 Production Readiness Notes

This project is development-focused. Before moving to production, the following steps are required:

- Replace SQLite with PostgreSQL/MySQL

- Add Alembic migrations

- Externalize secrets (JWT, DB credentials)

- Enforce HTTPS via reverse proxy (Nginx/Caddy)

- Add rate limiting & audit logging

- Enable monitoring and alerting

- Use Gunicorn + Uvicorn workers
----

https://github.com/user-attachments/assets/6b68cbc6-f2e3-4d19-9e7a-6cd64ef3bea9


https://github.com/user-attachments/assets/9d146901-1ba1-40b2-915b-a654580201bd

https://github.com/user-attachments/assets/47fc2a50-74ee-4db5-bfc9-3bbaf2ed4559

https://github.com/user-attachments/assets/192c214e-079a-47b7-81ed-7f8bcce25475


