from sqlalchemy import Column, Integer, String
from app.db import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    phone_number = Column(String, unique=True, index=True)   # login field
    pin_hash = Column(String, nullable=True)                 # hashed PIN
