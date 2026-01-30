from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .factories import create_customer, create_account

def test_customer_cannot_create_account(customer_client: TestClient, db: Session):
    user = create_customer(db)

    res = customer_client.post(
        "/accounts/",
        json={"customer_id": user.id, "initial_deposit": 200},
    )

    # unauthenticated OR forbidden are both valid outcomes
    assert res.status_code in (401, 403)



def test_admin_can_create_account(admin_client: TestClient, db: Session):
    user = create_customer(db)

    res = admin_client.post(
        "/accounts/",
        json={"customer_id": user.id, "initial_deposit": 1000},
    )

    assert res.status_code == 201
    assert res.json()["customer_id"] == user.id


def test_customer_cannot_access_other_balance(customer_client: TestClient, db: Session):
    user1 = create_customer(db)
    user2 = create_customer(db)

    acc1 = create_account(db, user1.id, 500)
    create_account(db, user2.id, 700)

    res = customer_client.get(f"/accounts/{acc1.id}/balance")

    assert res.status_code in (401, 403)



def test_staff_can_delete_account(staff_client: TestClient, db: Session):
    user = create_customer(db)
    acc = create_account(db, user.id)

    res = staff_client.delete(f"/accounts/{acc.id}")

    assert res.status_code in (200, 204)
