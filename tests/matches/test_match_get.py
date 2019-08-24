import json

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.serializers.matches import serialize_match


def test_match_returns_405_if_method_is_not_allowed(init_database, test_client):
    match_id = 1

    rv = test_client.put(f'/api/v1/matches/{match_id}/')
    assert rv.status_code == 405

    rv = test_client.delete(f'/api/v1/matches/{match_id}/')
    assert rv.status_code == 405


def test_match_returns_empty_response_when_there_are_match_with_that_id(init_database, test_client):
    match_id = 1

    rv = test_client.get(f'/api/v1/matches/{match_id}/')

    assert rv.status_code == 404
    assert b'' in rv.data


def test_match_returns_content_when_there_is_a_match_with_that_id(
        init_database, test_client, user1_username, user2_username, match):
    db.session.add(match)
    db.session.commit()

    expected_response = serialize_match(match)
    rv = test_client.get(f'/api/v1/matches/{match.id}/')

    assert rv.status_code == 200
    assert expected_response == json.loads(rv.data)
