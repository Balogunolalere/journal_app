from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.services.auth import get_user
from app.models.user import User

# Define constants
TOKEN_URL = "token"
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

# Define custom exception
class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Define OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

# Define a function to get the current user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get the current user from the provided token."""
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CredentialsException
    except JWTError:
        raise CredentialsException

    # Get the user from the database
    user = get_user(email)
    if user is None:
        raise CredentialsException

    # Return the user
    return User(key=user.key, email=user.email)
