from fastapi import HTTPException, status
import jwt
from app.config import settings
from app.models import User
from app import supabase, logger


def authenticate_user(user: User, password: str) -> tuple[str, str]:
    """
    Authenticates a user by verifying the provided
    password against the user's stored password.

    Args:
        user (User): The user object to authenticate.
        password (str): The password to verify.

    Returns:
        tuple[str, str]: A tuple containing the access token and refresh token.

    Raises:
        HTTPException: If the password is incorrect or
            the user's password is not set.
    """

    data = supabase.auth.sign_in_with_password(
        {
            "email": user.email,
            "password": password,
        }
    )

    if not data.session:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect password.",
        )

    access_token = data.session.access_token
    refresh_token = data.session.refresh_token

    return access_token, refresh_token


def verify_token(token: str) -> dict:
    config = settings.get()
    try:
        decoded_token = supabase.auth._decode_jwt(token)
        return decoded_token
    except jwt.PyJWTError as ex:
        logger.debug(config.jwt.secret)
        logger.exception(ex)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_refresh_token(token: str) -> dict:
    config = settings.get()
    try:
        decoded_token = jwt.decode(
            token,
            config.jwt.secret,
            algorithms=["HS256"],
        )
        return decoded_token
    except jwt.PyJWTError as ex:
        logger.exception(ex)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_access_token_from_refresh_token(
    refresh_token: str,
) -> str | None:
    data = verify_refresh_token(refresh_token)

    response = supabase.auth.refresh_session(data["refresh_token"])

    if not response.session:
        return None

    return response.session.access_token
