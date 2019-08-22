
def test_root_returns_200(test_client):
    rv = test_client.get('/')
    assert rv.status_code == 200

