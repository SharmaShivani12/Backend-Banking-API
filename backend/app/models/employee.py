from sqlalchemy import Column, Integer, String, Boolean
from app.db import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="employee")   # <-- REQUIRED
    is_active = Column(Boolean, default=True)

