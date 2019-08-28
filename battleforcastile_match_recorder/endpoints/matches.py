import json

from flask import request, abort
from flask_restful import Resource

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.metrics import num_of_matches_created_total
from battleforcastile_match_recorder.models import Match
from battleforcastile_match_recorder.serializers.matches import serialize_match
from battleforcastile_match_recorder.utils.get_match_if_available import get_match_if_available


class MatchListResource(Resource):
    def get(self):
        matches = Match.query.all()

        return [serialize_match(match) for match in matches], 200

    def post(self):
        status_code = 200
        data = json.loads(request.data) if request.data else {}

        second_user_username = None

        # Validate request
        if (
                not data.get('first_user') or
                not data.get('first_user').get('username') or
                not data.get('first_user').get('character')
        ):
            abort(400)
        first_user_username = data.get('first_user').get('username')

        # If second user is provided, we make sure that it has enough information to be used
        if data.get('second_user'):
            if (
                    not data.get('second_user').get('username') or
                    not data.get('second_user').get('character')
            ):
                abort(400)
            second_user_username = data.get('second_user').get('username')

        # If there's an existing match already created and not finished we don't create a new one. We just return 200
        existing_match = Match.query.filter_by(
            first_user_username=first_user_username, second_user_username=second_user_username, finished=False).first()

        if existing_match:
            match = existing_match
        else:
            status_code = 201

            match = Match(
                first_user_username=first_user_username,
                first_user_character=json.dumps(data['first_user']['character']),
                second_user_username=second_user_username,
                second_user_character=json.dumps(data['second_user']['character']) if second_user_username else None,
            )
            db.session.add(match)
            db.session.commit()
            num_of_matches_created_total.inc()

        return serialize_match(match), status_code


class SearchMatchResource(Resource):
    def post(self):
        data = json.loads(request.data) if request.data else {}

        # Validate request
        if (
                not data.get('user') or
                not data.get('user').get('username') or
                not data.get('user').get('character')
        ):
            abort(400)

        user_username = data.get('user').get('username')

        match = get_match_if_available(user_username)
        if match and not match.started:
            # If the user is the second user, we need to add it to the match info
            if match.first_user_username is not None and match.second_user_username is None:
                match.second_user_username = user_username
                match.second_user_character = json.dumps(data['user']['character'])
                db.session.add(match)
                db.session.commit()

            return serialize_match(match), 200

        # If there's no matches available
        return '', 204


class MatchResource(Resource):
    def get(self, match_id):
        match = Match.query.filter_by(id=match_id).first()
        if match:
            return serialize_match(match), 200
        return '', 404

    def patch(self, match_id):
        status_code = 200
        data = json.loads(request.data) if request.data else {}

        match = Match.query.filter_by(id=match_id).first()

        if not match:
            abort(404)

        # Validate request
        if data.get('first_user'):
            if (
                not data.get('first_user').get('username') or
                not data.get('first_user').get('character')
            ):
                abort(400)

            first_user_username = data.get('first_user').get('username')

            match.first_user_username = first_user_username
            match.first_user_character = json.dumps(data['first_user']['character'])
            db.session.add(match)
            db.session.commit()

        if data.get('second_user'):
            if (
                not data.get('second_user').get('username') or
                not data.get('second_user').get('character')
            ):
                abort(400)

            second_user_username = data.get('second_user').get('username')

            match.second_user_username = second_user_username
            match.second_user_character = json.dumps(data['second_user']['character'])
            db.session.add(match)
            db.session.commit()

        if data.get('winner_username'):
            winner = data.get('winner_username')

            match.winner_username = winner
            db.session.add(match)
            db.session.commit()

        if data.get('started'):
            match.started = data.get('started')
            db.session.add(match)
            db.session.commit()

        if data.get('finished'):
            match.finished = data.get('finished')
            db.session.add(match)
            db.session.commit()

        return serialize_match(match), status_code