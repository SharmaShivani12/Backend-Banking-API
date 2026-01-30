from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .factories import create_customer, create_account


def test_transfer_same_account(admin_client: TestClient, db: Session):
    user = create_customer(db)
    acc = create_account(db, user.id, balance=500)

    res = admin_client.post("/transfers/", json={
        "from_account_id": acc.id,
        "to_account_id": acc.id,
        "amount": 100
    })

    # validation error
    assert res.status_code in (400, 422)


def test_transfer_invalid_account(admin_client: TestClient, db: Session):
    sender = create_customer(db)
    acc1 = create_account(db, sender.id, balance=500)

    res = admin_client.post("/transfers/", json={
        "from_account_id": acc1.id,
        "to_account_id": 999999,
        "amount": 50
    })

    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()


def test_transfer_negative_amount(admin_client: TestClient, db: Session):
    sender = create_customer(db)
    receiver = create_customer(db)

    acc1 = create_account(db, sender.id, 300)
    acc2 = create_account(db, receiver.id, 100)

    res = admin_client.post("/transfers/", json={
        "from_account_id": acc1.id,
        "to_account_id": acc2.id,
        "amount": -50
    })

    assert res.status_code in (400, 422)
