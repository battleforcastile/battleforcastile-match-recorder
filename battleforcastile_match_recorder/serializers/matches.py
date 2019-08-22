def serialize_match(match):
    return {
        'id': match.id,
        'turns': [turn.id for turn in match.turns],
        'first_user': {
            'username': match.first_user.username,
            'character': match.first_user_character
        },
       'second_user': {
           'username': match.second_user.username if match.second_user else None,
           'character': match.second_user_character if match.second_user_character else None
       },
        'winner': match.winner.username if match.winner else None,
        'finished': match.finished
    }