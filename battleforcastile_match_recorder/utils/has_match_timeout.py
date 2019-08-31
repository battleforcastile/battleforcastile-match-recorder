import datetime

from battleforcastile_match_recorder.constants import MAX_NUM_SECONDS_SINCE_CREATION


def has_match_timeout(match):
    return False if match.created_at > datetime.datetime.utcnow() - datetime.timedelta(
        seconds=MAX_NUM_SECONDS_SINCE_CREATION) else True