from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerOut, CustomerLogin
from app.core.security import hash_pin, verify_pin, create_access_token

router = APIRouter(
    prefix="/customer/auth",
    tags=["🔐 Authentication (👤 Customer)"],
)

# ---------------- REGISTER ---------------- #
@router.post("/register", response_model=CustomerOut, status_code=201)
def customer_register(
    data: CustomerCreate,
    db: Session = Depends(get_db),
):
    exists = (
        db.query(Customer)
        .filter(Customer.phone_number == data.phone_number)
        .first()
    )
    if exists:
        raise HTTPException(400, "Phone number already registered")

    customer = Customer(
        name=data.name,
        phone_number=data.phone_number,
        pin_hash=hash_pin(data.pin),
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


# ---------------- LOGIN ---------------- #
@router.post("/login")
def customer_login(
    data: CustomerLogin,
    db: Session = Depends(get_db),
):
    user = (
        db.query(Customer)
        .filter(Customer.phone_number == data.phone_number)
        .first()
    )
    if not user or not verify_pin(data.pin, user.pin_hash):
        raise HTTPException(401, "Invalid phone or PIN")

    # sub MUST be string (JWT best practice)
    token = create_access_token(
        {"sub": str(user.id), "role": "customer"}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
