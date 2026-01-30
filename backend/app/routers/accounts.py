from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from pydantic import BaseModel


from app.db import get_db
from app.schemas.account import (
    AccountCreate,
    Account,
    BalanceResponse,
    AccountUpdate,
)
from app.models.account import Account as AccountModel
from app.models.customer import Customer as CustomerModel
from app.models.transfer import Transfer as TransferModel
from app.routers.auth import get_current_user
from app.config import settings
from app.core.permissions import require_role, require_owner_or_staff
from app.schemas.account import AccountOut
from app.core.token_utils import get_token_payload
from app.core.security import decode_token
from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")
router = APIRouter(
    prefix="/accounts",
    tags=["💳 Accounts"],
)

# ---------------- CREATE ACCOUNT ---------------- #
@router.post("/",summary="Create Account (👨‍💼Staff only)", response_model=Account, status_code=201)
def create_account(
    payload: AccountCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if settings.env == "prod":
        require_role(user, "admin", "employee")

    customer = db.query(CustomerModel).filter_by(id=payload.customer_id).first()
    if not customer:
        raise HTTPException(404, "Customer not found")

    account = AccountModel(
        customer_id=payload.customer_id,
        balance=payload.initial_deposit,
    )
    db.add(account)
    db.commit()
    db.refresh(account)

    return account


# ---------------- TRANSFER HISTORY ---------------- #
@router.get("/{account_id}/transfers", summary="👁️ View transfers by account (👨‍💼 Staff / 👤 Customer)")
def account_transfers(
    account_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2),
):
    data = decode_token(token)
    if not data:
        raise HTTPException(401, "Invalid token")

    acc = db.query(AccountModel).filter_by(id=account_id).first()
    if not acc:
        raise HTTPException(404, "Account not found")

    role = data["role"]

    # STAFF → full access
    if role in ("admin", "employee"):
        pass

    # CUSTOMER → only own account
    elif role == "customer":
        if acc.customer_id != int(data["sub"]):
            raise HTTPException(403, "Access denied")

    else:
        raise HTTPException(403, "Not allowed")

    transfers = (
        db.query(TransferModel)
        .filter(
            (TransferModel.from_account_id == account_id) |
            (TransferModel.to_account_id == account_id)
        )
        .order_by(TransferModel.created_at.desc())
        .all()
    )

    # ✅ THIS solves your requirement
    return [
        {
            "id": t.id,
            "from_account_id": t.from_account_id,
            "to_account_id": t.to_account_id,
            "amount": float(t.amount),
            "direction": "outgoing" if t.from_account_id == account_id else "incoming",
            "created_at": t.created_at.isoformat(),
        }
        for t in transfers
    ]


# ---------------- UPDATE ACCOUNT ---------------- #
@router.put("/{account_id}",summary="✏️ Update Account (👨‍💼Staff only)", response_model=Account)
def update_account(
    account_id: int,
    payload: AccountUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    acc = db.query(AccountModel).filter_by(id=account_id).first()
    if not acc:
        raise HTTPException(404, "Account not found")

    if settings.env == "prod":
        require_owner_or_staff(user, acc.customer_id)

    if payload.balance is not None:
        acc.balance = payload.balance

    db.commit()
    db.refresh(acc)

    return acc


# ---------------- DELETE ACCOUNT ---------------- #
@router.delete("/{account_id}",summary="❌ Deletion of Account (👨‍💼 Staff only)", status_code=204)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if settings.env == "prod":
        require_role(user, "admin", "employee")

    acc = db.query(AccountModel).filter_by(id=account_id).first()
    if not acc:
        raise HTTPException(404, "Account not found")

    db.delete(acc)
    db.commit()
    return None


# ---------------- DEPOSIT ---------------- #
@router.post("/{account_id}/deposit", summary="💰 Deposit in Account (👨‍💼 Staff only)")
def deposit(
    account_id: int,
    amount: Decimal,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if settings.env == "prod" and user.role not in ("admin", "employee"):
        raise HTTPException(403, "Staff only")

    acc = db.query(AccountModel).filter_by(id=account_id).first()
    if not acc:
        raise HTTPException(404, "Account not found")

    acc.balance += amount
    db.commit()
    db.refresh(acc)

    return {"balance": float(acc.balance)}


# ---------------- WITHDRAW ---------------- #
@router.post(
    "/{account_id}/withdraw",
    status_code=status.HTTP_200_OK,
    summary="💸 Withdraw money (👨‍💼Staff only)",
)
def withdraw(
    account_id: int,
    amount: Decimal,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if settings.env == "prod" and user.role not in ("admin", "employee"):
        raise HTTPException(403, "Staff only")

    acc = db.query(AccountModel).filter_by(id=account_id).first()
    if not acc:
        raise HTTPException(404, "Account not found")

    if amount <= 0:
        raise HTTPException(400, "Amount must be positive")

    if acc.balance < amount:
        raise HTTPException(400, "Insufficient funds")

    acc.balance -= amount
    db.commit()
    db.refresh(acc)

    return {
        "account_id": acc.id,
        "new_balance": float(acc.balance),
    }

# --------------------Listing accounts-----------
@router.get(
    "/",
    summary="🧾 Accounts List (👨‍💼Staff/👤Customer)",
    response_model=List[AccountOut],
)
def list_accounts(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2),
):
    data = decode_token(token)
    if not data:
        raise HTTPException(401, "Invalid token")

    role = data["role"]

    # STAFF → all accounts
    if role in ("admin", "employee"):
        return (
            db.query(AccountModel)
            .order_by(AccountModel.id)
            .all()
        )

    # CUSTOMER → only own accounts
    if role == "customer":
        customer_id = int(data["sub"])
        return (
            db.query(AccountModel)
            .filter(AccountModel.customer_id == customer_id)
            .order_by(AccountModel.id)
            .all()
        )

    raise HTTPException(403, "Not allowed")


# ---------------- Balance HISTORY ---------------- #

@router.get("/{account_id}/balance",summary="👁️View Balance (👨‍💼Staff/👤Customer)", response_model=BalanceResponse)
def get_balance(
    account_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2),
):
    data = decode_token(token)
    if not data:
        raise HTTPException(401, "Invalid token")

    acc = db.query(AccountModel).filter_by(id=account_id).first()
    if not acc:
        raise HTTPException(404, "Account not found")

    role = data["role"]

    # STAFF: allow
    if role in ("admin", "employee"):
        pass

    # CUSTOMER: must own account
    elif role == "customer":
        if acc.customer_id != int(data["sub"]):
            raise HTTPException(403, "Access denied")

    else:
        raise HTTPException(403)

    return BalanceResponse(
        account_id=acc.id,
        balance=acc.balance,
    )