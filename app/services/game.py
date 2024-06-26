from app.dao import DAO
from app.models import Game
from app.services.player import get_computer_player
import uuid


def create_game(
    dao: DAO,
    player1_id: str,
    player2_id: str | None = None,
) -> Game:
    computer_player = get_computer_player(dao)

    game = Game(
        id=str(uuid.uuid4()),
        player1_id=player1_id,
        player2_id=player2_id or computer_player.id,
    )

    dao.game.add(game)
    return game
