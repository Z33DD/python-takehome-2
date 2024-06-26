from fastapi import HTTPException
from app.models import Game, GameTurn, User, Marks
from app.dao import DAO
from sqlmodel import select


def new_turn(
    dao: DAO,
    game: Game,
    player: User,
    x: int,
    y: int,
) -> GameTurn:
    mark = Marks.X.value if player.id == game.player1_id else Marks.O.value

    validate_position(game, x, y)
    validate_mark(dao, game, player, mark)
    validate_last_turn_player(dao, game, player)

    state = game.serialize_state()
    state[x][y] = mark
    game.deserialize_state(state)

    dao.game.add(game)

    new_turn = GameTurn(
        game_id=game.id,
        player_id=player.id,
        x=x,
        y=y,
        mark=mark,
    )
    dao.game_turn.add(new_turn)

    return new_turn


def validate_last_turn_player(dao, game, player) -> None:
    stmt = (
        select(GameTurn)
        .where(GameTurn.game_id == game.id)
        .order_by(
            GameTurn.created_at.desc(),
        )
    )
    last_turn = dao.game_turn.session.exec(stmt).first()
    if not last_turn:
        if player.id != game.player1_id:
            raise HTTPException(
                status_code=400,
                detail="It's not your turn",
            )
        return

    if last_turn.player_id == player.id:
        raise HTTPException(
            status_code=400,
            detail="It's not your turn",
        )


def validate_position(game: Game, x: int, y: int) -> None:
    state = game.serialize_state()

    if state[x][y] != Marks.EMPTY.value:
        raise HTTPException(
            status_code=400,
            detail="Position already taken",
        )
    if not (0 <= x <= 2 and 0 <= y <= 2):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid position: {x}, {y}",
        )


def validate_mark(dao, game, player, mark) -> None:
    if mark != Marks.X.value and mark != Marks.O.value:
        raise HTTPException(
            status_code=400,
            detail="Invalid mark",
        )
    stmt = (
        select(GameTurn)
        .where(GameTurn.game_id == game.id)
        .where(GameTurn.player_id == player.id)
        .where(GameTurn.mark != mark)
        .limit(1)
    )
    incorrect_marks = dao.game_turn.session.exec(stmt).all()
    if incorrect_marks:
        raise HTTPException(
            status_code=400,
            detail="Invalid mark",
        )


def get_player_by_mark(game: Game, mark: str) -> User:
    match mark:
        case Marks.X.value:
            return game.player1
        case Marks.O.value:
            return game.player2
        case _:
            raise ValueError("Invalid mark")


def check_winner(game: Game) -> User | None:
    state = game.serialize_state()
    # Check rows
    for row in state:
        if row.count(row[0]) == len(row) and row[0] != Marks.EMPTY.value:
            return get_player_by_mark(game, row[0])

    # Check columns
    for col in range(len(state[0])):
        if all(
            state[row][col] == state[0][col] and state[0][col] != Marks.EMPTY.value
            for row in range(len(state))
        ):
            return get_player_by_mark(game, state[0][col])

    # Check diagonals
    if state[0][0] == state[1][1] == state[2][2] and state[0][0] != Marks.EMPTY.value:
        return get_player_by_mark(game, state[0][0])
    if state[0][2] == state[1][1] == state[2][0] and state[0][2] != Marks.EMPTY.value:
        return get_player_by_mark(game, state[0][2])

    # No winner
    return None


def check_draw(game: Game) -> bool:
    state = game.serialize_state()
    return all(all(cell != Marks.EMPTY.value for cell in row) for row in state)
