import google.cloud.logging
import logging
import os

from battleforcastile_match_recorder.custom_formatter import CustomFormatter

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if os.getenv('PRODUCTION_MODE'):
    client = google.cloud.logging.Client()
    handler = client.get_default_handler()
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)

