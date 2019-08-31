import json

from flask import request, abort
from flask_restful import Resource, inputs
from flask_restful import reqparse

from battleforcastile_match_recorder.custom_logging import logging
from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.metrics import num_of_matches_created_total
from battleforcastile_match_recorder.models import Match
from battleforcastile_match_recorder.serializers.matches import serialize_match
from battleforcastile_match_recorder.utils.get_matches_available import get_matches_available
from battleforcastile_match_recorder.utils.has_match_timeout import has_match_timeout


class MatchListResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_user_username', type=str, required=False)
        parser.add_argument('started', type=inputs.boolean, required=False)
        parser.add_argument('finished', type=inputs.boolean, required=False)
        parser.add_argument('only_first', type=inputs.boolean, required=False)
        parser.add_argument('desc', type=inputs.boolean, required=False)

        args = parser.parse_args()

        qs = Match.query.filter()

        if args.get('first_user_username'):
            qs = qs.filter_by(first_user_username=args.get('first_user_username'))

        if args.get('started'):
            qs = qs.filter_by(started=args.get('started'))

        if args.get('finished'):
            qs = qs.filter_by(finished=args.get('finished'))

        if args.get('desc'):
            qs = qs.order_by(Match.created_at.desc())

        if args.get('only_first'):
            first_match = qs.first()
            matches = [first_match] if first_match else []
        else:
            matches = qs.all()

        return [serialize_match(match) for match in matches] if matches else [], 200

    def post(self):
        data = json.loads(request.data) if request.data else {}

        # Validate request
        if (
                not data.get('first_user') or
                not data.get('first_user').get('username') or
                not data.get('first_user').get('character')
        ):
            logging.info(
                f'[CREATE MATCH] Match could not be created due to missing information',
                {
                    'request_id': None,
                    'service': 'battleforcastile-match-recorder',
                    'username': None,
                    'action': 'create_match',
                    'payload': data
                }
            )
            abort(400)
        first_user_username = data.get('first_user').get('username')

        match = Match(
            first_user_username=first_user_username,
            first_user_character=json.dumps(data['first_user']['character']),
            started=False,
            finished=False
        )
        db.session.add(match)
        db.session.commit()
        logging.info(
            f'[CREATE MATCH] Match was created',
            {
                'request_id': None,
                'service': 'battleforcastile-match-recorder',
                'username': None,
                'action': 'create_match',
                'payload': data
            }
        )

        num_of_matches_created_total.inc()

        return serialize_match(match), 201


class JoinMatchResource(Resource):
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
        logging.info(
            f'[JOIN MATCH] User was looking for a Match',
            {
                'request_id': None,
                'service': 'battleforcastile-match-recorder',
                'username': None,
                'action': 'join_match',
                'payload': data
            }
        )

        matches_available = get_matches_available(user_username)
        for match in matches_available:
            if not has_match_timeout(match):
                logging.info(
                    f'[JOIN MATCH] Match was found. User has joined (as a second user)',
                    {
                        'request_id': None,
                        'service': 'battleforcastile-match-recorder',
                        'username': None,
                        'action': 'join_match',
                        'payload': data
                    }
                )
                match.second_user_username = user_username
                match.second_user_character = json.dumps(data['user']['character'])
                db.session.add(match)
                db.session.commit()

                return serialize_match(match), 200

        # If there's no matches available
        logging.info(
            f'[JOIN MATCH] No Matches were available to join',
            {
                'request_id': None,
                'service': 'battleforcastile-match-recorder',
                'username': None,
                'action': 'join_match',
                'payload': data
            }
        )
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
            logging.info(
                f'[UPDATE MATCH] Match was not found',
                {
                    'request_id': None,
                    'service': 'battleforcastile-match-recorder',
                    'username': None,
                    'action': 'update_match',
                    'payload': data
                }
            )
            abort(404)

        # Validate request
        if data.get('first_user'):
            if (
                not data.get('first_user').get('username') or
                not data.get('first_user').get('character')
            ):
                logging.info(
                    f'[UPDATE MATCH] Match could not be updated due to missing "first_user" information',
                    {
                        'request_id': None,
                        'service': 'battleforcastile-match-recorder',
                        'username': None,
                        'action': 'update_match',
                        'payload': data
                    }
                )
                abort(400)

            first_user_username = data.get('first_user').get('username')

            match.first_user_username = first_user_username
            match.first_user_character = json.dumps(data['first_user']['character'])

        if data.get('second_user'):
            if (
                not data.get('second_user').get('username') or
                not data.get('second_user').get('character')
            ):
                logging.info(
                    f'[UPDATE MATCH] Match could not be updated due to missing "second_user" information',
                    {
                        'request_id': None,
                        'service': 'battleforcastile-match-recorder',
                        'username': None,
                        'action': 'update_match',
                        'payload': data
                    }
                )
                abort(400)

            second_user_username = data.get('second_user').get('username')

            match.second_user_username = second_user_username
            match.second_user_character = json.dumps(data['second_user']['character'])

        if data.get('winner_username'):
            winner = data.get('winner_username')
            logging.info(
                f'[SET WINNER] User won the Match',
                {
                    'request_id': None,
                    'service': 'battleforcastile-match-recorder',
                    'username': None,
                    'action': 'update_match',
                    'payload': data
                }
            )
            match.winner_username = winner

        if data.get('started'):
            logging.info(
                f'[START MATCH] Match started',
                {
                    'request_id': None,
                    'service': 'battleforcastile-match-recorder',
                    'username': None,
                    'action': 'update_match',
                    'payload': data
                }
            )
            match.started = data.get('started')

        if data.get('finished'):
            logging.info(
                f'[FINISH MATCH] Match finished',
                {
                    'request_id': None,
                    'service': 'battleforcastile-match-recorder',
                    'username': None,
                    'action': 'update_match',
                    'payload': data
                }
            )
            match.finished = data.get('finished')

        db.session.add(match)
        db.session.commit()

        return serialize_match(match), status_code