from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal

from app.db import get_db
from app.models.account import Account as AccountModel
from app.models.transfer import Transfer as TransferModel
from app.schemas.transfer import TransferCreate, Transfer
from app.routers.auth import get_current_user
from app.config import settings
from sqlalchemy import or_
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(
    prefix="/transfers",
    tags=["🔁 Transfers"],
)

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def get_account(db: Session, acc_id: int) -> AccountModel:
    acc = db.query(AccountModel).filter_by(id=acc_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail=f"Account {acc_id} not found")
    return acc


# -------------------------------------------------
# Create transfer
# -------------------------------------------------
@router.post(
    "/",
    summary="💱 Create Transfer (👨‍💼 Staff / 👤 Customer)",
    response_model=Transfer,
    status_code=201,
)
def create_transfer(
    payload: TransferCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2),
):
    data = decode_token(token)
    if not data:
        raise HTTPException(401, "Invalid or expired token")

    role = data["role"]

    if role not in ("admin", "employee", "customer"):
        raise HTTPException(403, "Not allowed")

    from_acc = get_account(db, payload.from_account_id)
    to_acc = get_account(db, payload.to_account_id)

    # 👤 CUSTOMER: can only transfer from OWN account
    if role == "customer":
        customer_id = int(data["sub"])
        if from_acc.customer_id != customer_id:
            raise HTTPException(
                status_code=403,
                detail="Customers can only transfer from their own accounts",
            )

    if payload.from_account_id == payload.to_account_id:
        raise HTTPException(422, "Cannot transfer to same account")

    if from_acc.balance < payload.amount:
        raise HTTPException(400, "Insufficient funds")

    from_acc.balance -= payload.amount
    to_acc.balance += payload.amount

    transfer = TransferModel(
        from_account_id=payload.from_account_id,
        to_account_id=payload.to_account_id,
        amount=payload.amount,
    )

    db.add(transfer)
    db.commit()
    db.refresh(transfer)

    return transfer


# -------------------------------------------------
# List all transfers (staff only in prod)
# -------------------------------------------------
@router.get("/", summary=" 🧾 List all transfers (👨‍💼Staff only)",response_model=List[Transfer])
def list_transfers(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role == "customer":
        raise HTTPException(
            status_code=403,
            detail="Customers cannot view all transfers",
        )

    return (
        db.query(TransferModel)
        .order_by(TransferModel.created_at.desc())
        .all()
    )


# Listing of transfers by accounts
"""
@router.get(
    "/account/{account_id}",
    summary="👁️ View transfers by account (👨‍💼 Staff / 👤 Customer)",
    response_model=List[Transfer],
)
def list_transfers_by_account(
    account_id: int,
    token: str = Depends(oauth2),
    db: Session = Depends(get_db),
):
    data = decode_token(token)
    if not data:
        raise HTTPException(401, "Invalid or expired token")

    account = get_account(db, account_id)
    role = data["role"]

    # 👨‍💼 STAFF → unrestricted
    if role in ("admin", "employee"):
        pass

    # 👤 CUSTOMER → only own account
    elif role == "customer":
        customer_id = int(data["sub"])
        if account.customer_id != customer_id:
            raise HTTPException(
                status_code=403,
                detail="You can only view your own account transfers",
            )
    else:
        raise HTTPException(403, "Not allowed")

    transfers = (
        db.query(TransferModel)
        .filter(
            or_(
                TransferModel.from_account_id == account_id,
                TransferModel.to_account_id == account_id,
            )
        )
        .order_by(TransferModel.created_at.desc())
        .all()
    )

    # ✅ If no transfers → []
    return transfers

    """