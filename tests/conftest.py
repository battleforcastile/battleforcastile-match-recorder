import json

import pytest

from battleforcastile_match_recorder import create_app, db
from battleforcastile_match_recorder.models import Match, Turn, User


@pytest.fixture(scope='function')
def test_client():
    flask_app = create_app('testing_config.py')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='function')
def init_database():
    flask_app = create_app('testing_config.py')

    with flask_app.app_context():
        from battleforcastile_match_recorder.models import Turn, Match, User

        # Create the database and the database table
        db.create_all()

        yield db  # this is where the testing happens!

        db.drop_all()


@pytest.fixture(scope='function')
def user1():
    user = User(
        email='user1@example.com',
        username='user1',
        password='12345'
    )
    return user


@pytest.fixture(scope='function')
def user2():
    user = User(
        email='user2@example.com',
        username='user2',
        password='12345'
    )
    return user


@pytest.fixture(scope='function')
def turn(user1, user2, match):
    state = {
        'hero': {
            'value': 10
        },
        'board': [[], []],
        'enemy': {
            'value': 20
        },
        'num_cards_in_hand_left': 5
    }
    turn = Turn(
        match=match,
        number=1,
        hero=user1,
        enemy=user2,
        state=json.dumps(state)
    )
    return turn


@pytest.fixture(scope='function')
def match(user1, user2):
    character = {
        "meta": {
            "name": "Black Forest Elf",
            "class": "creatures"
        },
        "stats": {
            "level": 1
        },
        "powers": []
    }
    user = Match(
        first_user=user1,
        first_user_character=json.dumps(character),
        second_user=user2,
        second_user_character=json.dumps(character)
    )
    return user