from typing import Any, Generic, TypeVar
from sqlmodel import SQLModel, Session, select

from app.models import User, GameTurn, Game

T = TypeVar("T", bound=SQLModel)


class BaseDAO(Generic[T]):
    session: Session
    model_class: type[SQLModel]
    cache: dict[str, T] = {}

    def __init__(self, session: Session, model_class: type[SQLModel]) -> None:
        self.session = session
        self.model_class = model_class

    def add(self, instance: T) -> None:
        self.session.add(instance)
        self.cache.update({str(instance.id): instance})

    def get(self, id: str | int) -> T | None:
        instance = self.session.get(self.model_class, id)
        if instance:
            self.cache.update({str(id): instance})
        return instance

    def query(
        self,
        field: str,
        value: Any,
        offset: int = 0,
        limit: int = 100,
    ) -> list[T]:
        statement = select(self.model_class).where(field == value)
        paginated_statement = statement.offset(offset).limit(limit)
        results = self.session.exec(paginated_statement).all()

        instances = []
        for instance in results:
            instances.append(instance)
            self.cache.update({str(instance.id): instance})

        return instances

    def query_one(self, field: Any, value: Any) -> T | None:
        statement = select(self.model_class).where(field == value)
        instance = self.session.exec(statement).first()

        if instance:
            self.cache.update({str(instance.id): instance})

        return instance

    def all(self, offset: int = 0, limit: int = 100) -> list[T]:
        statement = select(self.model_class)
        paginated_statement = statement.offset(offset).limit(limit)
        results = self.session.exec(paginated_statement).all()

        instances = []
        for instance in results:
            instances.append(instance)
            self.cache.update({str(instance.id): instance})

        return instances

    def delete(self, id: int | str) -> None:
        instance = self.get(id)
        self.session.delete(instance)
        self.cache.pop(str(id))

    def commit(self):
        self.session.commit()


class DAO:
    session: Session
    user: BaseDAO[User]
    game: BaseDAO[Game]
    game_turn: BaseDAO[GameTurn]

    def __init__(self, session: Session):
        self.session = session
        self.user = BaseDAO[User](
            model_class=User,
            session=session,
        )
        self.game = BaseDAO[Game](
            model_class=Game,
            session=session,
        )
        self.game_turn = BaseDAO[GameTurn](
            model_class=GameTurn,
            session=session,
        )
