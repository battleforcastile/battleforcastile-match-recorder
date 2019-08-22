import json

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.serializers.turns import serialize_turn


def test_turns_returns_405_if_method_is_not_allowed(init_database, test_client):
    match_id = 1
    rv = test_client.put(f'/api/v1/matches/{match_id}/turns/')
    assert rv.status_code == 405

    rv = test_client.patch(f'/api/v1/matches/{match_id}/turns/')
    assert rv.status_code == 405

    rv = test_client.delete(f'/api/v1/matches/{match_id}/turns/')
    assert rv.status_code == 405


def test_turns_returns_empty_response_when_there_are_no_turns(init_database, test_client, user1, user2, match):
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(match)
    db.session.commit()

    rv = test_client.get(f'/api/v1/matches/{match.id}/turns/')
    assert b'' in rv.data


def test_turns_returns_content_when_there_are_turns(init_database, test_client, user1, user2, match, turn):
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(match)
    db.session.add(turn)
    db.session.commit()

    expected_response = [serialize_turn(turn)]
    rv = test_client.get(f'/api/v1/matches/{match.id}/turns/')
    assert expected_response == json.loads(rv.data)
