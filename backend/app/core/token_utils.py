from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_token_payload(token: str = Depends(oauth2)):
    data = decode_token(token)
    if not data:
        raise HTTPException(401, "Invalid or expired token")
    return data
