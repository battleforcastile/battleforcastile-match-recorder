import datetime
import json

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.models import Match


def test_join_match_if_there_are_matches_available(init_database, test_client, user1_username):
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

    # First, we create a match to choose from
    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match))
    assert rv.status_code == 201

    finding_match = {
        'user': {
            'username': 'random_username',
            'character': {
                "meta": {
                    "name": "Yellow Forest Elf",
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
    rv = test_client.post('/api/v1/matches/join/', data=json.dumps(finding_match))
    assert rv.status_code == 200


def test_join_match_returns_400_when_payload_is_incomplete(init_database, test_client):
    finding_match = {}
    rv = test_client.post('/api/v1/matches/join/', data=json.dumps(finding_match))

    assert rv.status_code == 400

    finding_match = {
        'user': None
    }
    rv = test_client.post('/api/v1/matches/join/', data=json.dumps(finding_match))

    assert rv.status_code == 400

    finding_match = {
        'user': {
            'username': 'username'
        }
    }
    rv = test_client.post('/api/v1/matches/join/', data=json.dumps(finding_match))

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
    rv = test_client.post('/api/v1/matches/join/', data=json.dumps(finding_match))

    assert rv.status_code == 400


def test_join_match_returns_204_if_there_are_no_matches_available(init_database, test_client):

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
    rv = test_client.post('/api/v1/matches/join/', data=json.dumps(finding_match))

    assert rv.status_code == 204


def test_join_match_returns_204_if_there_are_no_matches_recently_created(init_database, test_client, user1_username):
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

    # First, we create a match to choose from
    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match))
    assert rv.status_code == 201

    created_match = Match.query.filter_by(first_user_username=user1_username).first()
    created_match.created_at = datetime.datetime.utcnow() - datetime.timedelta(days=10)
    db.session.add(created_match)
    db.session.commit()

    finding_match = {
        'user': {
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

    rv = test_client.post('/api/v1/matches/join/', data=json.dumps(finding_match))
    assert rv.status_code == 204


def test_join_match_returns_204_if_the_only_match_available_is_finished(init_database, test_client, user1_username):
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

    # First, we create a match to choose from
    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match))
    assert rv.status_code == 201

    found_match = Match.query.filter_by(first_user_username=user1_username).first()
    found_match.finished = True
    db.session.add(found_match)
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
    rv = test_client.post('/api/v1/matches/join/', data=json.dumps(finding_match))

    assert rv.status_code == 204


def test_join_match_returns_204_if_the_only_match_available_is_started(init_database, test_client, user1_username):
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

    # First, we create a match to choose from
    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match))
    assert rv.status_code == 201

    # Now we add a random turn
    found_match = Match.query.filter_by(first_user_username=user1_username).first()
    found_match.started = True
    db.session.add(found_match)
    db.session.commit()

    # Finally we  try to fetch it, but it shouldn't be able as it has already started
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
    rv = test_client.post('/api/v1/matches/join/', data=json.dumps(finding_match))

    assert rv.status_code == 204


def test_join_match_returns_204_if_there_are_no_matches_available_because_the_same_user_has_create_them(
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
    assert rv.status_code == 201

    finding_match = {
        'user': {
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

    # Second, we make a request to search for free matches
    rv = test_client.post('/api/v1/matches/join/', data=json.dumps(finding_match))
    assert rv.status_code == 204
