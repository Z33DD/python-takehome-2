import os
import random
import pytest
from typing import Any, Callable, Generator, Optional
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session
from app.config import settings
from app.dao import DAO
from app import supabase
from app.models import (
    User,
    create_all_tables,
)
from app.server import app_factory
from faker import Faker


@pytest.fixture()
def test_client() -> Generator[TestClient, Any, None]:
    app = app_factory()
    yield TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def db_file():
    create_all_tables()
    yield
    os.remove("./db.sqlite")


@pytest.fixture()
def faker_seed():
    return random.randint(0, 100)


@pytest.fixture
def dao():
    config = settings.get()
    engine = config.build_engine()

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield DAO(session)
        session.commit()


@pytest.fixture
def user_factory(dao: DAO, faker: Faker, faker_seed) -> Callable[..., User]:
    def factory(password: Optional[str] = None) -> User:
        # Faker.seed(0)

        if not password:
            password = str(faker.password())

        randint = str(random.randint(0, 100))

        user = User(
            username=faker.user_name(),
            email=randint + faker.email(),
        )

        supabase.auth.sign_up(
            {
                "email": user.email,
                "password": password,
            }
        )
        dao.user.add(user)
        dao.user.commit()

        return user

    return factory
