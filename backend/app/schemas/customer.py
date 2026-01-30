from pydantic import BaseModel

# -----------------------------------------
# Create / Register customer schema
# -----------------------------------------
class CustomerCreate(BaseModel):
    name: str
    phone_number: str
    pin: str


# -----------------------------------------
# Used when returning customer info
# -----------------------------------------
class CustomerOut(BaseModel):
    id: int
    name: str
    phone_number: str | None = None

    class Config:
        from_attributes = True


# -----------------------------------------
# Login schema (needed by customer_auth.py)
# -----------------------------------------
class CustomerLogin(BaseModel):
    phone_number: str
    pin: str
