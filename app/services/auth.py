from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.db.base import user_base
from app.models.user import UserCreate, UserInDB, User
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(email: str):
    users = user_base.fetch({"email": email}).items
    if users:
        user_data = users[0]
        return UserInDB(**user_data)
    return None

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_user(user: UserCreate):
    db_user = get_user(user.email)
    if db_user:
        return None
    hashed_password = get_password_hash(user.password)
    new_user = UserInDB(
        key=uuid.uuid4().hex,
        email=user.email,
        hashed_password=hashed_password
    )
    user_base.put(new_user.dict())
    return User(key=new_user.key, email=new_user.email)

def update_user_password(email: str, new_password: str) -> User | None:
    user = get_user(email)
    if not user:
        return None
    
    updated_user = UserInDB(
        key=user.key,
        email=user.email,
        hashed_password=get_password_hash(new_password)
    )
    
    user_base.update(updated_user.dict(), user.key)
    return User(key=updated_user.key, email=updated_user.email)

def delete_user_from_db(email: str) -> bool:
    user = get_user(email)
    if not user:
        return False
    
    user_base.delete(user.key)
    return True