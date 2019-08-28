import json

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.models import Match
from battleforcastile_match_recorder.serializers.matches import serialize_match


def test_patch_match_returns_405_if_method_is_not_allowed(init_database, test_client):
    match_id = 1

    rv = test_client.put(f'/api/v1/matches/{match_id}/')
    assert rv.status_code == 405

    rv = test_client.delete(f'/api/v1/matches/{match_id}/')
    assert rv.status_code == 405


def test_patch_match_returns_404_when_there_are_match_with_that_id(init_database, test_client):
    match_id = 1

    rv = test_client.patch(f'/api/v1/matches/{match_id}/')

    assert rv.status_code == 404
    assert b'' in rv.data


def test_patch_match_returns_200_when_the_first_user_provided_is_unknown(
        init_database, test_client, user1_username, user2_username, match):
    db.session.add(match)

    db.session.commit()

    changed_match = {
        'first_user': {
            'username': 'test',
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

    rv = test_client.patch(f'/api/v1/matches/{match.id}/', data=json.dumps(changed_match))

    assert rv.status_code == 200


def test_patch_match_returns_200_when_the_second_user_provided_is_unknown(
        init_database, test_client, user1_username, user2_username, match):
    db.session.add(match)

    db.session.commit()

    changed_match = {
        'second_user': {
            'username': 'test',
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

    rv = test_client.patch(f'/api/v1/matches/{match.id}/', data=json.dumps(changed_match))

    assert rv.status_code == 200


def test_patch_match_returns_400_when_payload_is_incomplete(
        init_database, test_client, user1_username, user2_username, match):
    db.session.add(match)

    db.session.commit()

    changed_match = {
        'first_user': {
            'username': 'test'
        }
    }
    rv = test_client.patch(f'/api/v1/matches/{match.id}/', data=json.dumps(changed_match))

    assert rv.status_code == 400

    changed_match = {
        'first_user': {
            'character': {}
        }
    }
    rv = test_client.patch(f'/api/v1/matches/{match.id}/', data=json.dumps(changed_match))

    assert rv.status_code == 400

    changed_match = {
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
    rv = test_client.patch(f'/api/v1/matches/{match.id}/', data=json.dumps(changed_match))

    assert rv.status_code == 400

    changed_match = {
        'second_user': {
            'username': 'test'
        }
    }
    rv = test_client.patch(f'/api/v1/matches/{match.id}/', data=json.dumps(changed_match))

    assert rv.status_code == 400

    changed_match = {
        'second_user': {
            'character': {}
        }
    }
    rv = test_client.patch(f'/api/v1/matches/{match.id}/', data=json.dumps(changed_match))

    assert rv.status_code == 400

    changed_match = {
        'second_user': {
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
    rv = test_client.patch(f'/api/v1/matches/{match.id}/', data=json.dumps(changed_match))

    assert rv.status_code == 400


def test_patch_match_returns_200_when_it_has_been_successfully_patched(
        init_database, test_client, user1_username, user2_username, match):
    db.session.add(match)

    db.session.commit()

    changed_match = {
        'first_user': {
            'username': user1_username,
            'character': {
                "meta": {
                    "name": "Black Forest Elf",
                    "class": "creatures"
                },
                "stats": {
                    "level": 10
                },
                "powers": []
            }
        },
        'second_user': {
            'username': user2_username,
            'character': {
                "meta": {
                    "name": "Black Forest Elf",
                    "class": "creatures"
                },
                "stats": {
                    "level": 10
                },
                "powers": []
            }
        },
        'winner_username': user1_username,
        'started': True,
        'finished': True
    }

    rv = test_client.patch(f'/api/v1/matches/{match.id}/', data=json.dumps(changed_match))

    modified_match = Match.query.filter_by(id=match.id).first()

    assert rv.status_code == 200
    assert serialize_match(modified_match) == json.loads(rv.data)
    assert str(changed_match['first_user']['character']['stats']['level']) in json.loads(
        rv.data)['first_user']['character']
    assert str(changed_match['second_user']['character']['stats']['level']) in json.loads(
        rv.data)['second_user']['character']
    assert user1_username == json.loads(rv.data)['winner_username']
    assert json.loads(rv.data)['started'] == True
    assert json.loads(rv.data)['finished'] == True