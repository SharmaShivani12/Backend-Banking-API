from pydantic import BaseModel, ConfigDict, Field, PositiveInt, condecimal, model_validator
from datetime import datetime
from pydantic import BaseModel, field_validator
from decimal import Decimal

class TransferCreate(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal = Field(gt=0)
    @field_validator("to_account_id")
    @classmethod
    def not_same_account(cls, v, info):
        if "from_account_id" in info.data and v == info.data["from_account_id"]:
            raise ValueError("Cannot transfer to same account")
        return v

class Transfer(BaseModel):
    id: PositiveInt
    from_account_id: PositiveInt
    to_account_id: PositiveInt
    amount: condecimal(max_digits=12, decimal_places=2) # type: ignore
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
