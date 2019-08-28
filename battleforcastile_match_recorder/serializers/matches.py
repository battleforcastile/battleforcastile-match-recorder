def serialize_match(match):
    return {
        'id': match.id,
        'turns': [turn.id for turn in match.turns],
        'first_user': {
            'username': match.first_user_username,
            'character': match.first_user_character
        },
       'second_user': {
           'username': match.second_user_username if match.second_user_username else None,
           'character': match.second_user_character if match.second_user_character else None
       },
        'winner_username': match.winner_username if match.winner_username else None,
        'started': match.finished,
        'finished': match.finished
    }