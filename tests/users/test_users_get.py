import json

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.serializers.users import serialize_user


def test_users_returns_405_if_method_is_not_allowed(init_database, test_client):
    rv = test_client.put('/api/v1/users/')
    assert rv.status_code == 405

    rv = test_client.patch('/api/v1/users/')
    assert rv.status_code == 405

    rv = test_client.delete('/api/v1/users/')
    assert rv.status_code == 405


def test_users_returns_empty_response_when_there_are_no_users(init_database, test_client):
    rv = test_client.get('/api/v1/users/')
    assert b'' in rv.data
    assert rv.status_code == 200


def test_users_returns_content_when_there_are_users(init_database, test_client, user1, user2):
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    rv = test_client.get('/api/v1/users/')
    assert serialize_user(user1) in json.loads(rv.data)
    assert serialize_user(user2) in json.loads(rv.data)

    assert rv.status_code == 200
