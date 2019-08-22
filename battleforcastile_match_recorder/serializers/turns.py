def serialize_turn(turn):
    return {
        'match': turn.match.id,
        'number': turn.number,
        'hero': turn.hero.username,
        'enemy': turn.enemy.username,
        'state': turn.state,
        'num_cards_in_hand_left': turn.num_cards_in_hand_left
    }