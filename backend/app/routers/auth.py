# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.db import get_db
from app.models.employee import Employee
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["🔐 Authentication (👨‍💼Staff)"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# =========================================================
# Employee registration
# =========================================================
@router.post("/register/employee", summary="Employee Registration",status_code=201)
def register_staff(
    email: str,
    password: str,
    role: str,
    db: Session = Depends(get_db),
):
    if role not in ("admin", "employee"):
        raise HTTPException(400, "Invalid role")

    exists = db.query(Employee).filter(Employee.email == email).first()
    if exists:
        raise HTTPException(400, "Employee already exists")

    user = Employee(
        email=email,
        hashed_password=hash_password(password),
        role=role,
    )
    db.add(user)
    db.commit()

    return {"message": f"{role} created", "email": email}


# =========================================================
# Employee login -> JWT
# =========================================================
@router.post("/token")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(Employee).filter(Employee.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token(
        {
            "sub": user.email,
            "role": user.role,
            "uid": user.id,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


# =========================================================
# Shared dependency → authenticated user (REAL JWT ONLY)
# =========================================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    data = decode_token(token)
    if not data:
        raise HTTPException(401, "Invalid or expired token")

    user = db.query(Employee).filter(Employee.email == data["sub"]).first()
    if not user:
        raise HTTPException(401, "User not found")

    return user


# =========================================================
# Require staff only
# =========================================================
def get_current_employee(user=Depends(get_current_user)):
    if user.role not in ("admin", "employee"):
        raise HTTPException(403, "Employee role required")
    return user


@router.post("/logout")
def logout():
    return JSONResponse(
        {"message": "Logged out. Please remove token on client."}
    )
