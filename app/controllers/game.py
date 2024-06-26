from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.models import Game, User
from app.dependencies import get_current_user, get_dao
from app.dao import DAO
from app.services import game

router = APIRouter(
    prefix="/game",
)


class CreateGameRequest(BaseModel):
    player1: str
    player2: str | None = None


@router.post("/")
def create_game(
    payload: CreateGameRequest,
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
) -> Game:
    return game.create_game(
        dao,
        payload.player1,
        payload.player2,
    )


@router.get("/{game_id}")
async def get_game(
    game_id: str,
    dao: DAO = Depends(get_dao),
) -> Game:
    game = dao.game.get(game_id)
    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found",
        )
    return game


@router.get("/")
async def list_games(
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
) -> list[Game]:
    player1_list = dao.game.query(Game.player1_id, user.id)
    player2_list = dao.game.query(Game.player2_id, user.id)

    return player1_list + player2_list
