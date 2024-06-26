from random import random
from celery import Celery

from app.dao import DAO
from app.models import Game, Marks
from app.services.turn import new_turn
from app.config import settings
from sqlmodel import Session


# Create a Celery app
def worker_factory():
    config = settings.get()
    worker = Celery(
        "worker",
        broker=config.redis_dsn,
    )

    return worker


app = worker_factory()


# Define tasks
@app.task
def new_computer_turn(game: Game):
    config = settings.get()
    engine = config.build_engine()

    with Session(engine) as session:
        dao = DAO(session)
        # Get the current state of the game
        state = game.serialize_state()

        # Find all available positions
        available_positions = []
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == Marks.EMPTY.value:
                    available_positions.append((i, j))

        # Choose a random available position
        x, y = random.choice(available_positions)

        new_turn(dao, game, game.player2, x, y)
        session.commit()
