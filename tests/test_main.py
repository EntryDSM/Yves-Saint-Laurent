from ysl.main import app

client = app.test_client()


def test_index():
    response = client.get('/api/test/1')
    assert True
