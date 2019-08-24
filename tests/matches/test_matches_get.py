import json

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.serializers.matches import serialize_match


def test_matches_returns_405_if_method_is_not_allowed(init_database, test_client):
    rv = test_client.put('/api/v1/matches/')
    assert rv.status_code == 405

    rv = test_client.patch('/api/v1/matches/')
    assert rv.status_code == 405

    rv = test_client.delete('/api/v1/matches/')
    assert rv.status_code == 405

def test_matches_returns_empty_response_when_there_are_no_matches(init_database, test_client):
    rv = test_client.get('/api/v1/matches/')

    assert rv.status_code == 200
    assert b'' in rv.data


def test_matches_returns_content_when_there_are_matches(
        init_database, test_client, user1_username, user2_username, match, turn):
    db.session.add(match)
    db.session.add(turn)
    db.session.commit()

    expected_response = [serialize_match(match)]
    rv = test_client.get('/api/v1/matches/')
    assert expected_response == json.loads(rv.data)
