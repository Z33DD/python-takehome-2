from typing import Callable
from app.dao import DAO

from app.models import User
from app.services import auth


def test_create_token_with_a_user(
    dao: DAO,
    user_factory: Callable[..., User],
):
    password = "password"
    user = user_factory(password)
    assert user.id is not None

    token, _ = auth.authenticate_user(user, password)
    payload = auth.verify_token(token)
    del user

    user_email = payload.get("email")
    assert user_email is not None

    user = dao.user.query_one(User.email, user_email)

    assert user is not None
