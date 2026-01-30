from .factories import create_customer, create_account


def test_create_account(admin_client, db):
    customer = create_customer(db)

    res = admin_client.post("/accounts/", json={
        "customer_id": customer.id,
        "initial_deposit": 500
    })

    assert res.status_code == 201
    data = res.json()
    assert data["customer_id"] == customer.id
    assert float(data["balance"]) == 500


def test_get_balance(admin_client, db):
    customer = create_customer(db)
    account = create_account(db, customer.id, 700)

    res = admin_client.get(f"/accounts/{account.id}/balance")
    assert res.status_code == 200
    assert float(res.json()["balance"]) == 700.0


def test_update_account(admin_client, db):
    customer = create_customer(db)
    account = create_account(db, customer.id, 300)

    res = admin_client.put(
        f"/accounts/{account.id}",
        json={"balance": 900}
    )
    assert res.status_code == 200
    assert float(res.json()["balance"]) == 900


def test_delete_account(admin_client, db):
    customer = create_customer(db)
    account = create_account(db, customer.id)

    res = admin_client.delete(f"/accounts/{account.id}")
    assert res.status_code == 204


def test_transfer_history_empty(admin_client, db):
    customer = create_customer(db)
    account = create_account(db, customer.id)

    res = admin_client.get(f"/accounts/{account.id}/transfers")
    assert res.status_code == 200
    assert res.json() == []
