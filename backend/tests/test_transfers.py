from .factories import create_customer, create_account


def test_successful_transfer(admin_client, db):
    sender = create_customer(db)
    receiver = create_customer(db)

    acc1 = create_account(db, sender.id, balance=1000)
    acc2 = create_account(db, receiver.id, balance=200)

    res = admin_client.post("/transfers/", json={
        "from_account_id": acc1.id,
        "to_account_id": acc2.id,
        "amount": 300
    })

    assert res.status_code == 201

    bal1 = admin_client.get(f"/accounts/{acc1.id}/balance").json()["balance"]
    bal2 = admin_client.get(f"/accounts/{acc2.id}/balance").json()["balance"]

    assert float(bal1) == 700
    assert float(bal2) == 500


def test_insufficient_balance(admin_client, db):
    sender = create_customer(db)
    receiver = create_customer(db)

    acc1 = create_account(db, sender.id, balance=100)
    acc2 = create_account(db, receiver.id, balance=200)

    res = admin_client.post("/transfers/", json={
        "from_account_id": acc1.id,
        "to_account_id": acc2.id,
        "amount": 500
    })

    assert res.status_code == 400
    assert res.json()["detail"] == "Insufficient funds"


def test_transfer_history_after_operation(admin_client, db):
    sender = create_customer(db)
    receiver = create_customer(db)

    acc1 = create_account(db, sender.id, balance=800)
    acc2 = create_account(db, receiver.id, balance=100)

    admin_client.post("/transfers/", json={
        "from_account_id": acc1.id,
        "to_account_id": acc2.id,
        "amount": 250
    })

    history = admin_client.get(f"/accounts/{acc1.id}/transfers").json()
    assert len(history) == 1
