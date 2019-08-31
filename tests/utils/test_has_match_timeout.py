import datetime

from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.models import Match
from battleforcastile_match_recorder.utils.has_match_timeout import has_match_timeout


def test_if_has_match_timeout_is_true(init_database, user1_username, user2_username):
    character1 = '{}'
    character2 = '{}'

    match1 = Match(
        first_user_username=user1_username, first_user_character=character1,
        second_user_username=user2_username, second_user_character=character2)
    db.session.add(match1)
    db.session.commit()

    match1.created_at = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
    db.session.add(match1)
    db.session.commit()

    assert has_match_timeout(match1) is True


def test_if_has_match_timeout_is_false(init_database, user1_username, user2_username):
    character1 = '{}'
    character2 = '{}'

    match1 = Match(
        first_user_username=user1_username, first_user_character=character1,
        second_user_username=user2_username, second_user_character=character2)

    db.session.add(match1)
    db.session.commit()

    assert has_match_timeout(match1) is False
