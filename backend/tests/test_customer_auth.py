def test_register_customer(client):
    payload = {
        "name": "Alice",
        "phone_number": "9991112222",
        "pin": "1234",
    }

    res = client.post("/customer/auth/register", json=payload)

    assert res.status_code == 201
    assert res.json()["name"] == "Alice"


def test_register_duplicate_phone(client):
    client.post(
        "/customer/auth/register",
        json={
            "name": "User A",
            "phone_number": "8884441111",
            "pin": "1111",
        },
    )

    res = client.post(
        "/customer/auth/register",
        json={
            "name": "User B",
            "phone_number": "8884441111",
            "pin": "2222",
        },
    )

    assert res.status_code == 400
    assert res.json()["detail"] == "Phone number already registered"


def test_login_success(client):
    client.post(
        "/customer/auth/register",
        json={
            "name": "LoginUser",
            "phone_number": "7770009999",
            "pin": "5555",
        },
    )

    res = client.post(
        "/customer/auth/login",
        json={
            "phone_number": "7770009999",
            "pin": "5555",
        },
    )

    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_invalid_pin(client):
    client.post(
        "/customer/auth/register",
        json={
            "name": "LoginUserFail",
            "phone_number": "6660009999",
            "pin": "8888",
        },
    )

    res = client.post(
        "/customer/auth/login",
        json={
            "phone_number": "6660009999",
            "pin": "0000",
        },
    )

    assert res.status_code == 401
