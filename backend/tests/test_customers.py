def test_create_customer(admin_client):
    payload = {
        "name": "Alice",
        "phone_number": "9991113333",
        "pin": "1234",
    }

    res = admin_client.post("/customers/", json=payload)

    assert res.status_code == 201
    data = res.json()

    assert data["name"] == "Alice"
    assert data["phone_number"] == "9991113333"
    assert "id" in data


def test_multiple_customers(admin_client):
    res1 = admin_client.post("/customers/", json={
        "name": "User1",
        "phone_number": "9990011111",
        "pin": "1111",
    })
    res2 = admin_client.post("/customers/", json={
        "name": "User2",
        "phone_number": "9990011112",
        "pin": "2222",
    })

    assert res1.status_code == 201
    assert res2.status_code == 201
    assert res1.json()["id"] != res2.json()["id"]
