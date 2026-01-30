from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from app.config import settings

# ------------------------------
# Hashing Context
# ------------------------------
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------- PASSWORD HASHING (for employees)
def hash_password(password: str) -> str:
    return pwd.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd.verify(password, hashed)

# Backward compatible alias (fix import error from main.py)
def get_password_hash(pw: str):
    return hash_password(pw)


# -------- PIN HASHING (for customer PIN auth, later use)
def hash_pin(pin: str):
    return pwd.hash(pin)

def verify_pin(pin: str, hashed_pin: str):
    return pwd.verify(pin, hashed_pin)


# ------------------------------
# JWT Token Generator/Decoder
# ------------------------------
def create_access_token(data: dict, expires_minutes=settings.access_token_expire_minutes):
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    data.update({"exp": expire})
    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def decode_token(token: str):
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except:
        return None
