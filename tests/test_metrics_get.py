
def test_metrics_returns_200(test_client):
    rv = test_client.get('/metrics')
    assert rv.status_code == 200

