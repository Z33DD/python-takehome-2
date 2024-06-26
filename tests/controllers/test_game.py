import uuid
from typing import Callable
from fastapi.testclient import TestClient
from app.models import Game, User
from app.services import auth
from app.services.player import get_computer_player
from app.dao import DAO


def test_controller_create_game(
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    password = "password"
    user = user_factory(password)
    assert user.id is not None

    token, _ = auth.authenticate_user(user, password)

    player_1_id = str(uuid.uuid4())
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


def test_controller_create_game_versus_computer(
    dao: DAO,
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    password = "password"
    user = user_factory(password)
    assert user.id is not None

    token, _ = auth.authenticate_user(user, password)

    player_1_id = str(uuid.uuid4())
    computer_player = get_computer_player(dao)

    payload = {
        "player1": player_1_id,
        "player2": None,
    }
    expected_game = Game(
        player1_id=player_1_id,
        player2_id=computer_player.id,
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


def test_controller_get_game(
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    password = "password"
    user = user_factory(password)
    assert user.id is not None

    token, _ = auth.authenticate_user(user, password)

    player_1_id = str(uuid.uuid4())
    player_2_id = str(uuid.uuid4())

    payload = {
        "player1": player_1_id,
        "player2": player_2_id,
    }

    response = test_client.post(
        "/game",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    game_id = data["id"]

    response = test_client.get(
        f"/game/{game_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()

    assert response.status_code == 200, data
    assert data.get("id") is not None
    assert data["player1_id"] == player_1_id
    assert data["player2_id"] == player_2_id


def test_controller_get_all_games(
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

    response = test_client.post(
        "/game",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    game_id = data["id"]

    response = test_client.get(
        "/game/",
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()

    assert response.status_code == 200, data
    assert len(data) == 1
    assert data[0].get("id") is not None
    assert data[0]["player1_id"] == player_1_id
    assert data[0]["player2_id"] == player_2_id
    assert data[0]["id"] == game_id
