import json

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.models import Match
from battleforcastile_match_recorder.serializers.matches import serialize_match


def test_search_match_if_there_are_matches_available(init_database, test_client, user1):
    db.session.add(user1)
    db.session.commit()

    new_match = {
        'first_user': {
            'username': user1.username,
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

    # First, we create a match to choose from
    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match))
    assert rv.status_code == 201

    finding_match = {
        'user': {
            'username': 'random_username',
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

    # Second, we make a request to search for free matches
    rv = test_client.post('/api/v1/matches/search/', data=json.dumps(finding_match))
    assert rv.status_code == 200

    found_match = Match.query.filter_by(first_user=user1).filter(Match.second_user!=None).first()

    assert rv.status_code == 200
    assert serialize_match(found_match) == json.loads(rv.data)


def test_search_match_returns_400_when_payload_is_incomplete(init_database, test_client):
    finding_match = {}
    rv = test_client.post('/api/v1/matches/search/', data=json.dumps(finding_match))

    assert rv.status_code == 400

    finding_match = {
        'user': None
    }
    rv = test_client.post('/api/v1/matches/search/', data=json.dumps(finding_match))

    assert rv.status_code == 400

    finding_match = {
        'user': {
            'username': 'username'
        }
    }
    rv = test_client.post('/api/v1/matches/search/', data=json.dumps(finding_match))

    assert rv.status_code == 400

    finding_match = {
        'user': {
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
    rv = test_client.post('/api/v1/matches/search/', data=json.dumps(finding_match))

    assert rv.status_code == 400


def test_search_match_returns_204_if_there_are_no_matches_available(
        init_database, test_client, user1):
    db.session.add(user1)
    db.session.commit()

    finding_match = {
        'user': {
            'username': 'random_username',
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

    # Second, we make a request to search for free matches
    rv = test_client.post('/api/v1/matches/search/', data=json.dumps(finding_match))

    assert rv.status_code == 204


def test_search_match_returns_204_if_there_are_no_matches_available_because_the_same_user_has_create_them(
        init_database, test_client, user1):
    db.session.add(user1)
    db.session.commit()

    new_match = {
        'first_user': {
            'username': user1.username,
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
    assert rv.status_code == 201

    finding_match = {
        'user': {
            'username': user1.username,
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

    # Second, we make a request to search for free matches
    rv = test_client.post('/api/v1/matches/search/', data=json.dumps(finding_match))
    assert rv.status_code == 204
