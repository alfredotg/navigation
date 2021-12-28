from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify(plain_password, hashed_password) -> bool:
    return context.verify(plain_password, hashed_password)

def password_hash(password) -> str:
    return context.hash(password)

