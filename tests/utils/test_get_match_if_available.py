
from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.models import Match
from battleforcastile_match_recorder.utils.get_match_if_available import get_match_if_available


def test_get_match_if_available_if_all_matches_are_finished(init_database, user1, user2):
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    character1 = '{}'
    character2 = '{}'

    match1 = Match(
        first_user=user1, first_user_character=character1,
        second_user=user2, second_user_character=character2, finished=True)
    db.session.add(match1)
    db.session.commit()

    found_match = get_match_if_available(user1)

    assert found_match is None


def test_get_match_if_available_takes_match_already_assigned_where_user_is_assigned_as_first(init_database, user1, user2):
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    character1 = '{}'
    character2 = '{}'

    match1 = Match(
        first_user=user1, first_user_character=character1,
        second_user=user2, second_user_character=character2, finished=False)
    db.session.add(match1)
    db.session.commit()

    found_match = get_match_if_available(user1)

    assert found_match == match1


def test_get_match_if_available_takes_match_already_assigned_where_user_is_assigned_as_second(init_database, user1, user2):
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    character1 = '{}'
    character2 = '{}'

    match1 = Match(
        first_user=user1, first_user_character=character1,
        second_user=user2, second_user_character=character2, finished=False)
    db.session.add(match1)
    db.session.commit()

    found_match = get_match_if_available(user2)

    assert found_match == match1


def test_get_match_if_available_takes_match_with_a_free_slot(init_database, user1, user2):
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    character1 = '{}'

    match1 = Match(
        first_user=user1, first_user_character=character1, finished=False)
    db.session.add(match1)
    db.session.commit()

    found_match = get_match_if_available(user2)

    assert found_match == match1

def test_get_match_if_available_if_there_are_matches_but_the_matches_were_all_created_by_the_same_user(
        init_database, user1):
    db.session.add(user1)
    db.session.commit()

    character = '{}'

    match1 = Match(first_user=user1, first_user_character=character)
    db.session.add(match1)
    db.session.commit()

    found_match = get_match_if_available(user1)

    assert found_match is None


def test_get_match_if_available_if_there_are_no_matches(init_database, user2):
    db.session.add(user2)
    db.session.commit()

    found_match = get_match_if_available(user2)

    assert found_match is None
