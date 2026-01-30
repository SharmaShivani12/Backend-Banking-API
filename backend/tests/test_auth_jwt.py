from .factories import create_customer

def auth_as_admin(client):
    client.headers.update({
        "Authorization": "Bearer admin-token"
    })

# ---------------------------------------------------------
# Test 1 — Auth is required for protected endpoints
# ---------------------------------------------------------

def test_protected_account_create_requires_auth(client):
    """
    Unauthenticated users must not be able to create accounts
    """
    res = client.post("/accounts/", json={
        "customer_id": 1,
        "initial_deposit": 500
    })

    assert res.status_code == 401


# ---------------------------------------------------------
# Test 2 — Customer role cannot create account
# ---------------------------------------------------------

def test_customer_cannot_create_account(customer_client, db):
    """
    Customers are not allowed to create bank accounts
    """
    customer = create_customer(db)

    res = customer_client.post("/accounts/", json={
        "customer_id": customer.id,
        "initial_deposit": 500
    })

    # unauthenticated OR forbidden
    assert res.status_code in (401, 403)


# ---------------------------------------------------------
# Test 3 — Employee can create account
# ---------------------------------------------------------
def test_employee_can_create_account(staff_client, db):
    customer = create_customer(db)

    res = staff_client.post("/accounts/", json={
        "customer_id": customer.id,
        "initial_deposit": 500
    })

    assert res.status_code == 201


# ---------------------------------------------------------
# Test 4 — Admin can create account
# ---------------------------------------------------------

def test_admin_can_create_account(admin_client, db):
    customer = create_customer(db)

    res = admin_client.post("/accounts/", json={
        "customer_id": customer.id,
        "initial_deposit": 500
    })

    assert res.status_code == 201

