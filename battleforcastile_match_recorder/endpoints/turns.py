import json

from flask import request, abort
from flask_restful import Resource

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.models import Turn, User, Match
from battleforcastile_match_recorder.serializers.turns import serialize_turn


class TurnListResource(Resource):
    def get(self, match_id):
        turns = Turn.query.filter(Turn.match.has(id=match_id)).all()

        return [serialize_turn(turn) for turn in turns], 200

    def post(self, match_id):
        data = json.loads(request.data) if request.data else {}

        # Validate request
        if (
                not data.get('number') or
                not data.get('hero') or
                not data.get('enemy') or
                not data.get('state') or
                data.get('num_cards_in_hand_left') is None
        ):
            abort(400)

        match = Match.query.filter_by(id=match_id).first()
        if not match:
            abort(400)

        hero = User.query.filter_by(username=data['hero']).first()
        enemy = User.query.filter_by(username=data['enemy']).first()

        turn = Turn(
            match=match,
            number=data['number'],
            hero=hero,
            enemy=enemy,
            state=json.dumps(data['state']),
            num_cards_in_hand_left=data['num_cards_in_hand_left']
        )
        try:
            db.session.add(turn)
            db.session.commit()
        except Exception:
            return '', 204

        return serialize_turn(turn), 201


class TurnResource(Resource):
    def get(self, match_id, turn_number, hero_username):
        turn = Turn.query.filter(Turn.match.has(id=match_id)).filter(
            Turn.hero.has(username=hero_username)).filter_by(number=turn_number).first()
        if turn:
            return serialize_turn(turn), 200
        return '', 404
