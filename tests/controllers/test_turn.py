import uuid
from typing import Callable
from fastapi.testclient import TestClient
from app.models import Game, User
from app.services import auth
from app.dao import DAO


def test_controller_new_turn(
    dao: DAO,
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    password = "password"
    user = user_factory(password)
    assert user.id is not None

    token, _ = auth.authenticate_user(user, password)

    player_1_id = str(user.id)
    player_2_id = str(uuid.uuid4())

    payload = {
        "player1": player_1_id,
        "player2": player_2_id,
    }
    expected_game = Game(
        player1_id=player_1_id,
        player2_id=player_2_id,
    )

    response = test_client.post(
        "/game",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()

    assert response.status_code == 200, data
    assert data.get("id") is not None
    assert data["player1_id"] == str(expected_game.player1_id)
    assert data["player2_id"] == str(expected_game.player2_id)

    game_id = data["id"]

    payload = {
        "game_id": game_id,
        "x": 0,
        "y": 0,
    }

    response = test_client.post(
        "/turn",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 200, data
    assert data.get("id") is not None

    turn = dao.game_turn.get(data["id"])
    assert turn is not None
    assert str(turn.game_id) == game_id
    assert str(turn.player_id) == player_1_id
    assert turn.x == 0
    assert turn.y == 0
    assert turn.mark.value == "X"


def test_controller_get_winner(
    dao: DAO,
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    password = "password"
    user = user_factory(password)
    assert user.id is not None
    token, _ = auth.authenticate_user(user, password)
    player_1_id = str(user.id)
    player_2_id = str(uuid.uuid4())
    payload = {
        "player1": player_1_id,
        "player2": player_2_id,
    }
    expected_game = Game(
        player1_id=player_1_id,
        player2_id=player_2_id,
    )
    response = test_client.post(
        "/game",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 200, data
    assert data.get("id") is not None
    assert data["player1_id"] == str(expected_game.player1_id)
    assert data["player2_id"] == str(expected_game.player2_id)
    game_id = data["id"]
    payload = {
        "game_id": game_id,
        "x": 0,
        "y": 0,
    }
    response = test_client.post(
        "/turn",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 200, data
    assert data.get("id") is not None
    turn = dao.game_turn.get(data["id"])
    assert turn is not None
    assert str(turn.game_id) == game_id
    assert str(turn.player_id) == player_1_id
    assert turn.x == 0
    assert turn.y == 0
    assert turn.mark.value == "X"

    response = test_client.get(
        f"/turn/winner/{game_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 400, data
    assert data.get("detail") == "No winner yet"


def test_controller_get_draw(
    dao: DAO,
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    password = "password"
    user = user_factory(password)
    assert user.id is not None
    token, _ = auth.authenticate_user(user, password)
    player_1_id = str(user.id)
    player_2_id = str(uuid.uuid4())
    payload = {
        "player1": player_1_id,
        "player2": player_2_id,
    }
    expected_game = Game(
        player1_id=player_1_id,
        player2_id=player_2_id,
    )
    response = test_client.post(
        "/game",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 200, data
    assert data.get("id") is not None
    assert data["player1_id"] == str(expected_game.player1_id)
    assert data["player2_id"] == str(expected_game.player2_id)
    game_id = data["id"]
    payload = {
        "game_id": game_id,
        "x": 0,
        "y": 0,
    }
    response = test_client.post(
        "/turn",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 200, data
    assert data.get("id") is not None
    turn = dao.game_turn.get(data["id"])
    assert turn is not None
    assert str(turn.game_id) == game_id
    assert str(turn.player_id) == player_1_id
    assert turn.x == 0
    assert turn.y == 0
    assert turn.mark.value == "X"

    response = test_client.get(
        f"/turn/draw/{game_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 400, data
    assert data.get("detail") == "No draw yet"


def test_controller_get_turns(
    dao: DAO,
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    password = "password"
    user = user_factory(password)
    assert user.id is not None
    token, _ = auth.authenticate_user(user, password)
    player_1_id = str(user.id)
    player_2_id = str(uuid.uuid4())
    payload = {
        "player1": player_1_id,
        "player2": player_2_id,
    }
    expected_game = Game(
        player1_id=player_1_id,
        player2_id=player_2_id,
    )
    response = test_client.post(
        "/game",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 200, data
    assert data.get("id") is not None
    assert data["player1_id"] == str(expected_game.player1_id)
    assert data["player2_id"] == str(expected_game.player2_id)
    game_id = data["id"]
    payload = {
        "game_id": game_id,
        "x": 0,
        "y": 0,
    }
    response = test_client.post(
        "/turn",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 200, data
    assert data.get("id") is not None
    turn = dao.game_turn.get(data["id"])
    assert turn is not None
    assert str(turn.game_id) == game_id
    assert str(turn.player_id) == player_1_id
    assert turn.x == 0
    assert turn.y == 0
    assert turn.mark.value == "X"
    response = test_client.get(
        f"/turn/{game_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 200, data
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0].get("id") == str(turn.id)
    assert data[0].get("game_id") == game_id
    assert data[0].get("player_id") == player_1_id
    assert data[0].get("x") == 0
    assert data[0].get("y") == 0
    assert data[0].get("mark") == "X"
