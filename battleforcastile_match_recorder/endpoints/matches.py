import google.cloud.logging
import datetime
import json
import os

from flask import request, abort
from flask_restful import Resource

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.constants import MAX_NUM_SECONDS_SINCE_CREATION
from battleforcastile_match_recorder.metrics import num_of_matches_created_total
from battleforcastile_match_recorder.models import Match
from battleforcastile_match_recorder.serializers.matches import serialize_match
from battleforcastile_match_recorder.utils.get_matches_available import get_matches_available

if os.getenv('SECRET_KEY'):
    client = google.cloud.logging.Client()
    client.setup_logging()

import logging


class MatchListResource(Resource):
    def get(self):
        matches = Match.query.all()

        return [serialize_match(match) for match in matches], 200

    def post(self):
        status_code = 200
        data = json.loads(request.data) if request.data else {}

        # Validate request
        if (
                not data.get('first_user') or
                not data.get('first_user').get('username') or
                not data.get('first_user').get('character')
        ):
            abort(400)
        first_user_username = data.get('first_user').get('username')
        logging.info(f'[CREATE MATCH] {first_user_username} is trying to create a new Match')

        # If there's an existing match already created and not finished we don't create a new one. We just return 200
        existing_match = Match.query.filter_by(
            first_user_username=first_user_username, started=False, finished=False).first()

        if existing_match and existing_match.created_at > datetime.datetime.utcnow() - datetime.timedelta(
                        seconds=MAX_NUM_SECONDS_SINCE_CREATION):
            logging.info(
                f'[CREATE MATCH] Match with {existing_match.first_user_username} (as a first user) already exists and waits for another user')

            match = existing_match
        else:
            status_code = 201

            match = Match(
                first_user_username=first_user_username,
                first_user_character=json.dumps(data['first_user']['character'])
            )
            db.session.add(match)
            db.session.commit()
            logging.info(f'[CREATE MATCH] Match with {match.first_user_username} (as a first user) has just been created')

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
        logging.info(f'[SEARCH MATCH] {user_username} is looking for a Match')

        matches_available = get_matches_available(user_username)
        for match in matches_available:
            logging.info(f'[SEARCH MATCH] Match {match.id} is a candidate. '
                         f'But it might have already started or be too old. '
                         f'Started: {match.started}. Created at: {match.created_at}')

            if (match and not match.started and
                    match.created_at > datetime.datetime.utcnow() - datetime.timedelta(
                        seconds=MAX_NUM_SECONDS_SINCE_CREATION)):

                # If the user is the second user, we need to add it to the match info
                if match.first_user_username is not None and match.second_user_username is None:
                    logging.info(f'[SEARCH MATCH] Match {match.id} was found. {user_username} is going to join (as a second user)')

                    match.second_user_username = user_username
                    match.second_user_character = json.dumps(data['user']['character'])
                    db.session.add(match)
                    db.session.commit()
                else:
                    logging.info(f'[SEARCH MATCH] Match {match.id} was found. It has already both participants:'
                                 f'First user {match.first_user_username}, Second user {match.second_user_username}')

                return serialize_match(match), 200

        # If there's no matches available
        logging.info(f'[SEARCH MATCH] No Matches are available at this moment')

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
            logging.info(f'[SET WINNER] {winner} has won Match {match.id}')

            match.winner_username = winner
            db.session.add(match)
            db.session.commit()

        if data.get('started'):
            logging.info(f'[START MATCH] Match {match.id} has just been started')

            match.started = data.get('started')
            db.session.add(match)
            db.session.commit()

        if data.get('finished'):
            logging.info(f'[FINISH MATCH] Match {match.id} has just been finished')

            match.finished = data.get('finished')
            db.session.add(match)
            db.session.commit()

        return serialize_match(match), status_code