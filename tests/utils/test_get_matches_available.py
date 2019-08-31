
from battleforcastile_match_recorder import db
from battleforcastile_match_recorder.models import Match
from battleforcastile_match_recorder.utils.get_matches_available import get_matches_available


def test_get_matches_available_if_all_matches_are_finished(init_database, user1_username, user2_username):
    character1 = '{}'
    character2 = '{}'

    match1 = Match(
        first_user_username=user1_username, first_user_character=character1,
        second_user_username=user2_username, second_user_character=character2, finished=True)
    db.session.add(match1)
    db.session.commit()

    found_matches = get_matches_available(user1_username)

    assert found_matches == []


def test_get_matches_available_if_all_matches_are_started(init_database, user1_username, user2_username):
    character1 = '{}'
    character2 = '{}'

    match1 = Match(
        first_user_username=user1_username, first_user_character=character1,
        second_user_username=user2_username, second_user_character=character2, started=True)
    db.session.add(match1)
    db.session.commit()

    found_matches = get_matches_available(user1_username)

    assert found_matches == []

def test_get_matches_available_returns_match_with_a_free_slot(
        init_database, user1_username, user2_username):

    character1 = '{}'

    match1 = Match(
        first_user_username=user1_username, first_user_character=character1, started=False, finished=False)
    db.session.add(match1)
    db.session.commit()

    found_matches = get_matches_available(user2_username)

    assert found_matches == [match1]

def test_get_matches_available_if_there_are_matches_but_the_matches_were_all_created_by_the_same_user(
        init_database, user1_username):

    character = '{}'

    match1 = Match(first_user_username=user1_username, first_user_character=character)
    db.session.add(match1)
    db.session.commit()

    found_matches = get_matches_available(user1_username)

    assert found_matches == []


def test_get_matches_available_if_there_are_no_matches(init_database, user2_username):

    found_matches = get_matches_available(user2_username)

    assert found_matches == []
