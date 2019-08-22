import random

from battleforcastile_match_recorder.models import Match


def get_match_if_available(user: str):
    if not user:
        raise Exception('No "user" provided')

    match = None
    # 1) Search for matches that have all opponents waiting, meaning the assignment has already been done
    # (And not finished)
    matches_ready_to_start_with_user_as_first_user = Match.query.filter_by(first_user=user, finished=False).filter(
        Match.second_user!=None).all()
    matches_ready_to_start_with_user_as_second_user = Match.query.filter_by(second_user=user, finished=False).filter(
        Match.first_user!=None).all()

    matches_ready_to_start = (
            matches_ready_to_start_with_user_as_first_user + matches_ready_to_start_with_user_as_second_user)

    if not matches_ready_to_start:
        # 2) If there's none, we look for other matches ready to join (with an open slot)
        matches_ready_to_start += Match.query.filter_by(second_user=None, finished=False).filter(
            Match.first_user!=user).all()

    if matches_ready_to_start:
        match = random.choice(matches_ready_to_start)

    return match