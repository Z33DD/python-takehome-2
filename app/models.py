from datetime import datetime
from enum import Enum
from uuid import uuid4, UUID
from sqlmodel import Relationship, SQLModel, Field
from app.config import settings
import json


def create_all_tables() -> None:
    config = settings.get()
    engine = config.build_engine()
    SQLModel.metadata.create_all(engine)


class Marks(Enum):
    EMPTY = "."
    X = "X"
    O = "O"  # noqa: E741


DEFAULT_GAME_STATE = json.dumps(
    [[Marks.EMPTY.value for _ in range(3)] for _ in range(3)]
)


class User(SQLModel, table=True):
    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
    )
    username: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class GameTurn(SQLModel, table=True):
    __tablename__ = "game_turn"
    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
    )
    game_id: UUID = Field(foreign_key="game.id")
    created_at: datetime = Field(default_factory=datetime.now)
    player_id: UUID = Field(foreign_key="user.id")
    mark: Marks

    x: int
    y: int


class Game(SQLModel, table=True):
    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
    )

    created_at: datetime = Field(default_factory=datetime.now)

    # In tic-tac-toe, we just have two players, so we can hardcode it here
    player1_id: UUID = Field(foreign_key="user.id")
    player2_id: UUID = Field(foreign_key="user.id")
    winner_id: UUID = Field(
        foreign_key="user.id",
        nullable=True,
        default=None,
    )

    # The current state of the game will be represented as a 2D array
    # serialized as a JSON string
    state: str = DEFAULT_GAME_STATE

    def serialize_state(self) -> list[list[str]]:
        return json.loads(self.state)

    def deserialize_state(self, state: list[list[str]]) -> None:
        self.state = json.dumps(state)

    turns: list[GameTurn] | None = Relationship()
