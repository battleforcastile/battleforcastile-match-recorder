import json

from flask import request, abort
from flask_restful import Resource

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.models import User
from battleforcastile_match_recorder.serializers.users import serialize_user


class UserListResource(Resource):
    def get(self):
        users = User.query.all()

        return [serialize_user(user) for user in users], 200

    def post(self):
        data = json.loads(request.data) if request.data else {}

        # Validate request
        if (
                not data.get('username') or
                not data.get('email') or
                not data.get('password')
        ):
            abort(400)

        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(user)
        db.session.commit()

        return serialize_user(user), 201
