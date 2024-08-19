from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.db.base import user_base
from app.models.user import UserCreate, UserInDB, User
import uuid

# Define constants
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Define password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define custom exception
class UserAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("User with this email already exists")

# Define a function to verify password
def verify_password(plain_password, hashed_password):
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# Define a function to get password hash
def get_password_hash(password):
    """Get the hashed password for a given password."""
    return pwd_context.hash(password)

# Define a function to get a user by email
def get_user(email: str):
    """Get a user by email."""
    users = user_base.fetch({"email": email}).items
    if users:
        user_data = users[0]
        return UserInDB(**user_data)
    return None

# Define a function to authenticate a user
def authenticate_user(email: str, password: str):
    """Authenticate a user by email and password."""
    user = get_user(email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# Define a function to create an access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create an access token for a given data."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Define a function to create a new user
def create_user(user: UserCreate):
    """Create a new user."""
    db_user = get_user(user.email)
    if db_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user.password)
    new_user = UserInDB(
        key=uuid.uuid4().hex,
        email=user.email,
        hashed_password=hashed_password
    )
    user_base.put(new_user.dict())
    return User(key=new_user.key, email=new_user.email)

# Define a function to update a user's password
def update_user_password(email: str, new_password: str) -> User | None:
    """Update a user's password."""
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

# Define a function to delete a user from the database
def delete_user_from_db(email: str) -> bool:
    """Delete a user from the database."""
    user = get_user(email)
    if not user:
        return False
    
    user_base.delete(user.key)
    return True
