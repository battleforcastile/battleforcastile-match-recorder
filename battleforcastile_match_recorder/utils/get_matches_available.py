from battleforcastile_match_recorder.models import Match


def get_matches_available(user_username: str):
    if not user_username:
        raise Exception('No "user" provided')

    # We look for other matches ready to join (with an open slot)
    matches_ready_to_start = Match.query.filter_by(second_user_username=None, started=False, finished=False).filter(
        Match.first_user_username!=user_username).order_by(Match.created_at.desc()).all()

    return matches_ready_to_start