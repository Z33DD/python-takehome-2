from faker import Faker
from app.dao import DAO
from app.models import User


def test_create_user(dao: DAO, faker: Faker, faker_seed):
    email = faker.email()
    username = faker.user_name()

    user = User(
        email=email,
        username=username,
    )

    dao.user.add(user)
    dao.user.commit()

    del user

    user = dao.user.query_one(User.email, email)

    assert user is not None
    assert user.email == email


def test_query_one_user(dao: DAO, faker: Faker, faker_seed):
    email = faker.email()
    username = faker.user_name()

    user = User(
        email=email,
        username=username,
    )

    dao.user.add(user)
    dao.user.commit()

    del user

    queried_user = dao.user.query_one(User.email, email)

    assert queried_user is not None


def test_query_one_user_not_exists(dao: DAO, faker: Faker, faker_seed):
    email = faker.email()

    queried_user = dao.user.query_one(User.email, email)

    assert queried_user is None
