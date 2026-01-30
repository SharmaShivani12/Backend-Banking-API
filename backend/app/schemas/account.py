from pydantic import BaseModel, ConfigDict, Field, PositiveInt, condecimal


# Base
class AccountBase(BaseModel):
    customer_id: PositiveInt = Field(..., description="Owner customer ID (must exist)")


# Payload for account creation
class AccountCreate(AccountBase):
    initial_deposit: condecimal(gt=0, max_digits=12, decimal_places=2) = Field(
        ..., description="Initial deposit must be positive"
    )


# Response model
class Account(AccountBase):
    id: PositiveInt
    balance: condecimal(max_digits=12, decimal_places=2) = Field(..., ge=0)

    model_config = ConfigDict(from_attributes=True)
# Account list 
class AccountOut(BaseModel):
    id: PositiveInt
    balance: condecimal(max_digits=12, decimal_places=2, ge=0)

    model_config = ConfigDict(from_attributes=True)

# Response only for balance endpoint
class BalanceResponse(BaseModel):
    account_id: PositiveInt
    balance: condecimal(max_digits=12, decimal_places=2, ge=0)

class AccountUpdate(BaseModel):
    balance: condecimal(gt=0, max_digits=12, decimal_places=2) | None = None
    customer_id: PositiveInt | None = None

    model_config = ConfigDict(from_attributes=True)
