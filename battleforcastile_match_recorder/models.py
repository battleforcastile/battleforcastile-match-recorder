from datetime import datetime

from battleforcastile_match_recorder import db


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turns = db.relationship('Turn', back_populates='match')

    first_user_username = db.Column(db.String(80), nullable=False)
    first_user_character = db.Column(db.Text, nullable=False)

    second_user_username = db.Column(db.String(80), nullable=True)
    second_user_character = db.Column(db.Text, nullable=True)

    winner_username = db.Column(db.String(80), nullable=True)

    finished = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return f'<Match {self.id} {self.created_at}>'


class Turn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    match = db.relationship('Match', foreign_keys=[match_id])
    number = db.Column(db.Integer, nullable=False)
    hero_username = db.Column(db.String(80), nullable=False)
    enemy_username = db.Column(db.String(80), nullable=False)

    state = db.Column(db.Text, nullable=False)
    num_cards_in_hand_left = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('number', 'match_id', 'hero_username', name='unique_constraint_commit'),
    )

    def __repr__(self):
        return f'<Turn {self.id} {self.number}>'