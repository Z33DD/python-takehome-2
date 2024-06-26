from app.models import User
from app.dao import DAO

COMPUTER_ID = "71ac5c8b-a057-40fa-ab4f-a297a5e2e769"


def get_computer_player(dao: DAO) -> User:
    user = dao.user.get(COMPUTER_ID)

    if user is None:
        user = User(
            id=COMPUTER_ID,
            username="computer",
            email="computer@example.com",
        )
        dao.user.add(user)

    return user
