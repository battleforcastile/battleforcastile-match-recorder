import json

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.models import Match
from battleforcastile_match_recorder.serializers.matches import serialize_match


def test_matches_are_successfully_created_when_passing_just_the_first_user(
        init_database, test_client, user1_username):

    new_match = {
        'first_user': {
            'username': user1_username,
            'character': {
                "meta": {
                    "name": "Black Forest Elf",
                    "class": "creatures"
                },
                "stats": {
                    "level": 1
                },
                "powers": []
            }
        }
    }

    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match))

    created_match = Match.query.filter_by(first_user_username=user1_username, second_user_username=None).first()

    assert rv.status_code == 201
    assert serialize_match(created_match) == json.loads(rv.data)


def test_matches_are_successfully_created_when_only_first_user_is_provided_and_user_needs_to_be_created(
        init_database, test_client):

    username = 'random_username'
    new_match = {
        'first_user': {
            'username': username,
            'character': {
                "meta": {
                    "name": "Black Forest Elf",
                    "class": "creatures"
                },
                "stats": {
                    "level": 1
                },
                "powers": []
            }
        }
    }
    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match))

    created_match = Match.query.filter_by(first_user_username=username, second_user_username=None).first()

    assert rv.status_code == 201
    assert serialize_match(created_match) == json.loads(rv.data)


def test_matches_returns_400_when_payload_is_incomplete(init_database, test_client, user1_username):

    new_match = {}
    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match))

    assert rv.status_code == 400

    new_match = {
        'first_user': None
    }
    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match))

    assert rv.status_code == 400

    new_match = {
        'first_user': {
            'username': 'username'
        }
    }
    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match))

    assert rv.status_code == 400

    new_match = {
        'first_user': {
            'character': {
                "meta": {
                    "name": "Black Forest Elf",
                    "class": "creatures"
                },
                "stats": {
                    "level": 1
                },
                "powers": []
            }
        }
    }
    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match))

    assert rv.status_code == 400
