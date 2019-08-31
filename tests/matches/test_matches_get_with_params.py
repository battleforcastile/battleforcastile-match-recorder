import json



def test_get_latest_non_started_match_created_by_username_if_there_are_matches_available(init_database, test_client, user1_username):
    new_match_1 = {
        'first_user': {
            'username': user1_username,
            'character': {
                "meta": {
                    "name": "Black Forest Elf",
                    "class": "creatures"
                },
                "stats": {
                    "level": 1
                },
                "powers": []
            }
        }
    }

    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match_1))
    assert rv.status_code == 201

    new_match_2 = {
        'first_user': {
            'username': user1_username,
            'character': {
                "meta": {
                    "name": "Yellow Forest Elf",
                    "class": "creatures"
                },
                "stats": {
                    "level": 1
                },
                "powers": []
            }
        }
    }

    rv = test_client.post('/api/v1/matches/', data=json.dumps(new_match_2))
    assert rv.status_code == 201


    rv = test_client.get(f'/api/v1/matches/?first_user_username={user1_username}&started=false&finished=false&desc=true&only_first=true')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert json.dumps(new_match_2['first_user']['character']) == (
        data[0]['first_user']['character'])


def test_get_matches_by_username_and_desc_returns_empty_list_if_there_are_no_matches_available(
        init_database, test_client, user1_username):
    rv = test_client.get(f'/api/v1/matches/?first_user_username={user1_username}&started=false&finished=false&desc=true&only_first=true')

    assert rv.status_code == 200
    assert json.loads(rv.data) == []