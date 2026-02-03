from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from typing import Optional
import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel


# Security scheme for API
security = HTTPBearer()


class TokenData(BaseModel):
    user_id: str
    exp: Optional[int] = None


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Verify the provided JWT token and return the user ID.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        TokenData: Contains the user ID and expiration

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        # Decode the token
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY", "fallback_secret_key"),
            algorithms=["HS256"]
        )

        user_id = payload.get("sub")
        exp = payload.get("exp")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        token_data = TokenData(user_id=user_id, exp=exp)

        # Check if token is expired
        if token_data.exp and datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )

        return token_data

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def create_access_token(user_id: str) -> str:
    """
    Create an access token for the user.

    Args:
        user_id: The user ID to include in the token

    Returns:
        str: JWT token
    """
    secret_key = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")

    expire = datetime.utcnow() + timedelta(minutes=30)  # Token expires in 30 minutes

    to_encode = {
        "sub": user_id,
        "exp": expire.timestamp()
    }

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def get_current_user_id(token_data: TokenData = Depends(verify_token)) -> str:
    """
    Get the current user's ID from the token.

    Args:
        token_data: Token data containing the user ID

    Returns:
        str: The user ID
    """
    return token_data.user_id


def validate_user_access(user_id: str, current_user_id: str = Depends(get_current_user_id)) -> bool:
    """
    Validate that the current user has access to the specified user_id.

    Args:
        user_id: The user ID to validate access to
        current_user_id: The current user's ID from the token

    Returns:
        bool: True if the user has access

    Raises:
        HTTPException: If the user doesn't have access
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )

    return True