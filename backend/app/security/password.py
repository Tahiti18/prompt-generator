from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_context():
    return _pwd_context

def verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)

def hash_password(plain: str) -> str:
    return _pwd_context.hash(plain)
