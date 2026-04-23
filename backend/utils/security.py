from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime , timedelta , timezone
import jwt
import os
from sqlmodel import Session, select
from models.users import UserInDB

oauth2_Scheme = OAuth2PasswordBearer(tokenUrl="token") 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Generate a cryptographically secure random key
# openssl rand -hex 32

# WHY:
# - Security systems need secrets that are impossible to guess
# - Humans are bad at creating randomness → use OpenSSL instead
# - This uses a cryptographically secure random number generator (CSPRNG)

# HOW:
# - Generates 32 random bytes from the OS entropy source
# - Converts each byte → 2 hex characters
# - Result = 64-character string (safe to copy, store, and use in configs)

# RESULT (example):
# e84ce4563c333c015132cff3d9fda4dc72da26580c587c0fc24eebf5b1852860
# Secret key used by your application for security operations

# WHY THIS EXISTS:
# - Your backend needs a "private secret" to prove data is trusted
# - Example: when issuing a JWT token, the server signs it using this key
# - Later, the server verifies the token using the SAME key
# → This ensures the token was not modified or forged

# HOW IT WORKS (JWT example):
# 1. Server creates payload:
#    { "user_id": 123 }
#
# 2. Server signs it using SECRET_KEY:
#    signature = HMAC(payload, SECRET_KEY)
#
# 3. Token = payload + signature
#
# 4. When client sends token back:
#    - Server recomputes signature using SECRET_KEY
#    - If match → token is valid
#    - If not → token is fake or tampered

# KEY IDEA:
# - Anyone WITHOUT SECRET_KEY cannot generate a valid signature
# - That’s why the key MUST be random and secret

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(session: Session, email: str, password: str):
    user = session.exec(select(UserInDB).where(UserInDB.email == email)).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user