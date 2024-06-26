from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import BaseModel

from app.models import User
from app.dependencies import get_current_user, get_dao
from app.dao import DAO
from app.services import turn
from app.services.player import COMPUTER_ID
from app.worker import new_computer_turn

router = APIRouter(
    prefix="/turn",
)


class NewTurnRequest(BaseModel):
    game_id: str
    x: int
    y: int


@router.post("/")
async def create_turn(
    payload: NewTurnRequest,
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
):
    game = dao.game.get(payload.game_id)
    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found",
        )

    new_turn = turn.new_turn(
        dao,
        game,
        user,
        payload.x,
        payload.y,
    )
    winner = turn.check_winner(game)
    if winner:
        return {"msg": f"Player {winner.email} wins!"}
    if turn.check_draw(game):
        return {"msg": "It's a draw!"}

    if game.player2_id == COMPUTER_ID:
        new_computer_turn.delay(game)
    return new_turn


@router.get("/winner/{game_id}")
async def get_winner(
    game_id: str,
    dao: DAO = Depends(get_dao),
):
    game = dao.game.get(game_id)
    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found",
        )

    winner = turn.check_winner(game)
    if not winner:
        raise HTTPException(
            status_code=400,
            detail="No winner yet",
        )
    return {"winner": winner.email}


@router.get("/draw/{game_id}")
async def get_draw(
    game_id: str,
    dao: DAO = Depends(get_dao),
):
    game = dao.game.get(game_id)
    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found",
        )

    if not turn.check_draw(game):
        raise HTTPException(
            status_code=400,
            detail="No draw yet",
        )
    return {"msg": "It's a draw!"}


@router.get("/{game_id}")
async def get_turns(
    game_id: str,
    dao: DAO = Depends(get_dao),
):
    game = dao.game.get(game_id)
    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found",
        )

    return game.turns  # turn.query_turns(dao, game)
