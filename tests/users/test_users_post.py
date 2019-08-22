import json

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.models import User
from battleforcastile_match_recorder.serializers.users import serialize_user


def test_users_are_successfully_created(init_database, test_client):
    new_user = {
        'username': 'blabla',
        'email': 'blabla@example.com',
        'password': '12345'
    }
    rv = test_client.post('/api/v1/users/', data=json.dumps(new_user))

    created_user = User.query.filter_by(username=new_user['username']).first()

    assert rv.status_code == 201
    assert serialize_user(created_user) == json.loads(rv.data)

def test_users_returns_400_when_payload_is_incomplete(init_database, test_client):
    new_user = {
        'email': 'blabla@example.com',
        'password': '12345'
    }
    rv = test_client.post('/api/v1/users/', data=json.dumps(new_user))

    assert rv.status_code == 400

    new_user = {
        'username': 'blabla',
        'password': '12345'
    }
    rv = test_client.post('/api/v1/users/', data=json.dumps(new_user))

    assert rv.status_code == 400

    new_user = {
        'email': 'blabla@example.com',
        'username': 'blabla'
    }
    rv = test_client.post('/api/v1/users/', data=json.dumps(new_user))

    assert rv.status_code == 400


