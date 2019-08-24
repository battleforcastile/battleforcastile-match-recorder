def serialize_turn(turn):
    return {
        'match': turn.match.id,
        'number': turn.number,
        'hero_username': turn.hero_username,
        'enemy_username': turn.enemy_username,
        'state': turn.state,
        'num_cards_in_hand_left': turn.num_cards_in_hand_left
    }