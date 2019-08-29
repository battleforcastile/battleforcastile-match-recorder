import os
import google.cloud.logging

import random

from battleforcastile_match_recorder.models import Match


if os.getenv('SECRET_KEY'):
    client = google.cloud.logging.Client()
    client.setup_logging()

import logging


def get_matches_available(user_username: str):
    if not user_username:
        raise Exception('No "user" provided')

    # 1) Search for matches that have all opponents waiting (and user is first user),
    # meaning the assignment has already been done (And not finished)
    matches_ready_to_start_with_user_as_first_user = Match.query.filter_by(
        first_user_username=user_username, started=False, finished=False).filter(
        Match.second_user_username != None).all()

    # 2) Search for matches that have all opponents waiting (and user is second user),
    # meaning the assignment has already been done (And not finished)
    matches_ready_to_start_with_user_as_second_user = Match.query.filter_by(
        second_user_username=user_username, started=False, finished=False).filter(
        Match.first_user_username != None).all()

    matches_ready_to_start = (
            matches_ready_to_start_with_user_as_first_user + matches_ready_to_start_with_user_as_second_user)

    if not matches_ready_to_start:
        # 2) If there's none, we look for other matches ready to join (with an open slot)
        matches_ready_to_start += Match.query.filter_by(
            second_user_username=None, started=False, finished=False).filter(
            Match.first_user_username!=user_username).all()

    return matches_ready_to_start