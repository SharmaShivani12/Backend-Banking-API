import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, get_db

TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine)


# -------------------- DB SETUP -------------------- #
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# -------------------- OVERRIDE get_db -------------------- #
@pytest.fixture(autouse=True)
def override_get_db(db):
    def _get_db():
        yield db
    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)
from app.models.employee import Employee
from app.models.customer import Customer
from app.core.security import hash_password, hash_pin


@pytest.fixture
def admin_client(client, db):
    admin = db.query(Employee).filter_by(email="admin@test.com").first()
    if not admin:
        admin = Employee(
            email="admin@test.com",
            hashed_password=hash_password("Admin123"),
            role="admin",
        )
        db.add(admin)
        db.commit()

    res = client.post(
        "/auth/token",
        data={"username": "admin@test.com", "password": "Admin123"},
    )

    token = res.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def staff_client(client, db):
    staff = db.query(Employee).filter_by(email="staff@test.com").first()
    if not staff:
        staff = Employee(
            email="staff@test.com",
            hashed_password=hash_password("Staff123"),
            role="employee",
        )
        db.add(staff)
        db.commit()

    res = client.post(
        "/auth/token",
        data={"username": "staff@test.com", "password": "Staff123"},
    )

    token = res.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def customer_client(client, db):
    customer = db.query(Customer).filter_by(phone_number="9998887777").first()
    if not customer:
        customer = Customer(
            name="Test Customer",
            phone_number="9998887777",
            pin_hash=hash_pin("1234"),
        )
        db.add(customer)
        db.commit()

    res = client.post(
        "/customer/auth/login",
        json={"phone_number": "9998887777", "pin": "1234"},
    )

    token = res.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
