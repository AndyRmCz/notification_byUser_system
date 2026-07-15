from datetime import datetime, timedelta, timezone
from jose import jwt
import bcrypt
from src.config.settings import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against an existing database string hash."""
    try:
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Generates a secure salt and hashes the plain text password natively."""
    # Convert password string to bytes
    password_bytes = password.encode('utf-8')
    # Generate a secure salt and hash the bytes
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    # Return as a string decode to store cleanly in SQLite/PostgreSQL
    return hashed_bytes.decode('utf-8')

def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)