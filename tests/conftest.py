import json

import pytest

from battleforcastile_match_recorder import create_app, db
from battleforcastile_match_recorder.models import Match, Turn


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
        from battleforcastile_match_recorder.models import Turn, Match

        # Create the database and the database table
        db.create_all()

        yield db  # this is where the testing happens!

        db.drop_all()


@pytest.fixture(scope='function')
def user1_username():
    return 'user1'


@pytest.fixture(scope='function')
def user2_username():
    return 'user2'


@pytest.fixture(scope='function')
def turn(user1_username, user2_username, match):
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
        hero_username=user1_username,
        enemy_username=user2_username,
        state=json.dumps(state)
    )
    return turn


@pytest.fixture(scope='function')
def match(user1_username, user2_username):
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
        first_user_username=user1_username,
        first_user_character=json.dumps(character),
        second_user_username=user2_username,
        second_user_character=json.dumps(character)
    )
    return user