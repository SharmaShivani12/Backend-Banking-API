from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerOut
from app.core.security import hash_pin
from app.routers.auth import get_current_user
from app.config import settings

router = APIRouter(
    prefix="/customers",
    tags=["👨‍💼 Customer Management"],
)


@router.post("/", summary="🟢 Create Customer Profile (👨‍💼Staff only)"
,response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # ---- RBAC: staff only in prod ----
    if settings.env == "prod" and user.role not in ("admin", "employee"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff can create customer profiles",
        )

    # ---- prevent duplicate phone ----
    existing = (
        db.query(Customer)
        .filter(Customer.phone_number == payload.phone_number)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone already registered",
        )

    customer = Customer(
        name=payload.name,
        phone_number=payload.phone_number,
        pin_hash=hash_pin(payload.pin),
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer

# Listing of customers 
from typing import List

@router.get("/",summary="🧾 List all Customers (👨‍💼Staff only)", response_model=List[CustomerOut])
def list_customers(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # ---- RBAC: staff only in prod ----
    if settings.env == "prod" and user.role not in ("admin", "employee"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff can view customers",
        )

    return db.query(Customer).order_by(Customer.id).all()
