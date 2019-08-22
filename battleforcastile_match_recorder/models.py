from datetime import datetime

from battleforcastile_match_recorder import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.id} {self.username}>'


users = db.Table('users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True)
)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turns = db.relationship('Turn', back_populates='match')

    first_user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    first_user = db.relationship('User',
        backref=db.backref('first_user_matches', lazy=True), foreign_keys=[first_user_id])
    first_user_character = db.Column(db.Text, nullable=False)
    second_user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=True)
    second_user = db.relationship('User',
        backref=db.backref('second_user_matches', lazy=True), foreign_keys=[second_user_id])
    second_user_character = db.Column(db.Text, nullable=True)

    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    winner = db.relationship('User',
        backref=db.backref('winner_matches', lazy=True), foreign_keys=[winner_id])

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
    hero_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    hero = db.relationship('User',
        backref=db.backref('hero_turns', lazy=True), foreign_keys=[hero_id])
    enemy_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    enemy = db.relationship('User',
        backref=db.backref('enemy_turns', lazy=True), foreign_keys=[enemy_id])
    state = db.Column(db.Text, nullable=False)
    num_cards_in_hand_left = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('number', 'match_id', 'hero_id', name='unique_constraint_commit'),
    )

    def __repr__(self):
        return f'<Turn {self.id} {self.number}>'