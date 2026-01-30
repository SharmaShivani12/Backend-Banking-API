from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.openapi.utils import get_openapi

from app.db import Base, engine, SessionLocal
from app.models.employee import Employee
from app.core.security import hash_password
from app.models.customer import Customer
from app.routers import auth, customers, accounts, transfers, customer_auth
from app.config import settings

# ---------------------------------------

public_tags = ["🔐 Authentication (👨‍💼Staff)", "🔐 Authentication (👤 Customer)"]  # no-lock

# ---------------------------------------

app = FastAPI(
    title="🏦 Banking API",
    description="""
Internal Banking API.

Roles:
- **👨‍💼 admin**: Full access
- **👨‍💼 employee**: Customer & account operations
- **👤 customer**: View own accounts, transfers

Actions are handled by (👨‍💼Staff /👤Customer)

Authentication:
- JWT Bearer Token required for protected endpoints
""",
    version="1.0.0",
)

# ---------------------------------------
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------
# DB
Base.metadata.create_all(bind=engine)


# ---------------------------------------
# Seed admin + sample customers

@app.on_event("startup")
def seed_admin_employee():
    db: Session = SessionLocal()
    try:
        if db.query(Employee).count() == 0:
            admin = Employee(
                email="admin@bank.com",
                hashed_password=hash_password("Admin123!"),
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("\n✔ Admin User Created Automatically\n")
    finally:
        db.close()


@app.on_event("startup")
def seed_initial_customers():
    db: Session = SessionLocal()
    try:
        if db.query(Customer).count() == 0:
            for c in [
                {"id": 1, "name": "Arisha Barron"},
                {"id": 2, "name": "Branden Gibson"},
                {"id": 3, "name": "Rhonda Church"},
                {"id": 4, "name": "Georgina Hazel"},
            ]:
                db.add(Customer(**c))
            db.commit()
            print("✔ Sample customers added.\n")
    finally:
        db.close()


# ---------------------------------------
# Routers
app.include_router(auth.router)
app.include_router(customer_auth.router)
app.include_router(customers.router)
app.include_router(accounts.router)
app.include_router(transfers.router)


# ---------------------------------------
# Root
@app.get("/")
def root():
    return {"status": "running", "message": "Banking API live"}


# ---------------------------------------
# Custom OpenAPI to show 🔒 lock only for protected routes

protected_tags = ["💳 Accounts", "🔁 Transfers", "👨‍💼 Customer Management"]
 # must match router tags exactly

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
    title=app.title,
    version=app.version,
    description=app.description,  # ← THIS is the fix
    routes=app.routes,
)


    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Add 🔒 lock to any route under protected tags
    for path, methods in schema.get("paths", {}).items():
        for method, details in methods.items():
            tags = details.get("tags", [])
            if any(tag in protected_tags for tag in tags):
                details["security"] = [{"BearerAuth": []}]   # << key line
            else:
                details.pop("security", None)

    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
