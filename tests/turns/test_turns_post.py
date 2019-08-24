import json

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.models import Turn
from battleforcastile_match_recorder.serializers.turns import serialize_turn


def test_turns_are_successfully_created(
        init_database, test_client, user1_username, user2_username, match):
    db.session.add(match)
    db.session.commit()

    new_turn = {
        'number': 1,
        'hero_username': user1_username,
        'enemy_username': user2_username,
        'state': {
            'hero': {
                'value': 10
            },
            'board': [[], []],
            'enemy': {
                'value': 20
            }
        },
        'num_cards_in_hand_left': 5
    }
    rv = test_client.post(f'/api/v1/matches/{match.id}/turns/', data=json.dumps(new_turn))
    created_turn = Turn.query.filter_by(match=match).first()
    assert serialize_turn(created_turn) == json.loads(rv.data)
    assert rv.status_code == 201


def test_turns_returns_400_if_match_doesnt_exist(
        init_database, test_client, user1_username, user2_username):
    db.session.commit()

    unknown_match_id = 123
    new_turn = {
        'number': 1,
        'hero_username': user1_username,
        'enemy_username': user2_username,
        'state': {
            'hero': {
                'value': 10
            },
            'board': [[], []],
            'enemy': {
                'value': 20
            }
        },
        'num_cards_in_hand_left': 5
    }
    rv = test_client.post(f'/api/v1/matches/{unknown_match_id}/turns/', data=json.dumps(new_turn))
    assert rv.status_code == 400


def test_turns_returns_204_if_turn_already_exists(
        init_database, test_client, user1_username, user2_username, match, turn):
    db.session.add(match)
    db.session.add(turn)
    db.session.commit()

    new_turn = {
        'number': turn.number,
        'hero_username': user1_username,
        'enemy_username': user2_username,
        'state': {
            'hero': {
                'value': 10
            },
            'board': [[], []],
            'enemy': {
                'value': 20
            }
        },
        'num_cards_in_hand_left': 5
    }
    rv = test_client.post(f'/api/v1/matches/{match.id}/turns/', data=json.dumps(new_turn))
    assert rv.status_code == 204


def test_turns_returns_400_when_payload_is_incomplete(
        init_database, test_client, user1_username, user2_username, match, turn):
    db.session.add(match)
    db.session.add(turn)

    db.session.commit()

    new_turn = {}
    rv = test_client.post(f'/api/v1/matches/{match.id}/turns/', data=json.dumps(new_turn))

    assert rv.status_code == 400

    new_turn = {
        'number': 1,
        'hero_username': user1_username,
        'enemy_username': user2_username,
        'num_cards_in_hand_left': 5
    }
    rv = test_client.post(f'/api/v1/matches/{match.id}/turns/', data=json.dumps(new_turn))

    assert rv.status_code == 400


    new_turn = {
        'number': 1,
        'hero_username': user1_username,
        'state': {
            'hero': {
                'value': 10
            },
            'board': [[], []],
            'enemy': {
                'value': 20
            }
        },
        'num_cards_in_hand_left': 5
    }
    rv = test_client.post(f'/api/v1/matches/{match.id}/turns/', data=json.dumps(new_turn))

    assert rv.status_code == 400

    new_turn = {
        'number': 1,
        'enemy_username': user2_username,
        'state': {
            'hero': {
                'value': 10
            },
            'board': [[], []],
            'enemy': {
                'value': 20
            }
        },
        'num_cards_in_hand_left': 5
    }
    rv = test_client.post(f'/api/v1/matches/{match.id}/turns/', data=json.dumps(new_turn))

    assert rv.status_code == 400

    new_turn = {
        'hero_username': user1_username,
        'enemy_username': user2_username,
        'state': {
            'hero': {
                'value': 10
            },
            'board': [[], []],
            'enemy': {
                'value': 20
            }
        },
        'num_cards_in_hand_left': 5
    }
    rv = test_client.post(f'/api/v1/matches/{match.id}/turns/', data=json.dumps(new_turn))

    assert rv.status_code == 400

    new_turn = {
        'number': 1,
        'hero_username': user1_username,
        'enemy_username': user2_username,
        'state': {
            'hero': {
                'value': 10
            },
            'board': [[], []],
            'enemy': {
                'value': 20
            }
        },
    }
    rv = test_client.post(f'/api/v1/matches/{match.id}/turns/', data=json.dumps(new_turn))

    assert rv.status_code == 400