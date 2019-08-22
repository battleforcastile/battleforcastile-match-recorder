import json

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.serializers.turns import serialize_turn


def test_turn_returns_405_if_method_is_not_allowed(init_database, test_client):
    match_id = 1
    turn_number = 1
    hero_username = 'test'

    rv = test_client.put(f'/api/v1/matches/{match_id}/turns/{turn_number}/hero/{hero_username}/')
    assert rv.status_code == 405

    rv = test_client.patch(f'/api/v1/matches/{match_id}/turns/{turn_number}/hero/{hero_username}/')
    assert rv.status_code == 405

    rv = test_client.delete(f'/api/v1/matches/{match_id}/turns/{turn_number}/hero/{hero_username}/')
    assert rv.status_code == 405


def test_turn_returns_empty_response_when_there_are_no_turns_with_that_number_and_hero(
        init_database, test_client, user1, user2, match):
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(match)
    db.session.commit()
    turn_number = 1

    rv = test_client.get(f'/api/v1/matches/{match.id}/turns/{turn_number}/hero/{user1.username}/')

    assert rv.status_code == 404
    assert b'' in rv.data


def test_turn_returns_empty_response_when_there_are_turns_with_that_number_but_not_hero(
        init_database, test_client, user1, user2, match, turn):
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(match)
    db.session.add(turn)
    db.session.commit()

    random_username = 'test'

    rv = test_client.get(f'/api/v1/matches/{match.id}/turns/{turn.number}/hero/{random_username}/')

    assert rv.status_code == 404
    assert b'' in rv.data


def test_turn_returns_content_when_there_are_turns_with_that_number_and_hero(
        init_database, test_client, user1, user2, match, turn):
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(match)
    db.session.add(turn)
    db.session.commit()

    expected_response = serialize_turn(turn)
    rv = test_client.get(f'/api/v1/matches/{match.id}/turns/{turn.number}/hero/{user1.username}/')

    assert rv.status_code == 200
    assert expected_response == json.loads(rv.data)
