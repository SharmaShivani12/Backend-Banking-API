# backend/tests/factories.py
import random
from app.models.customer import Customer
from app.models.account import Account
from app.core.security import hash_pin

def create_customer(db, name="Test User", pin="1234"):
    phone = str(random.randint(6000000000, 9999999999))
    user = Customer(
        name=name,
        phone_number=phone,
        pin_hash=hash_pin(pin),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_account(db, customer_id, balance=1000):
    acc = Account(customer_id=customer_id, balance=balance)
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc
