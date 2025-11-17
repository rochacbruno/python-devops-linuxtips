def test_root(client):
    result = client.get("/")
    assert result.status_code == 200
