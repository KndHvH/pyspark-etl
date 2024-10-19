import pytest
from models.connection_models import PostgresConnectionModel, APIConnectionModel

@pytest.mark.parametrize("host, user, password, database", [
    ('host', 'user', 'pass', 'database')
])
def test_postgres_connection_model(host, user, password, database):
    model = PostgresConnectionModel(host, user, password, database)
    assert model.host == host
    assert model.user == user
    assert model.password == password
    assert model.database == database

@pytest.mark.parametrize("url", [
    ('http://example.com')
])
def test_api_connection_model(url):
    model = APIConnectionModel(url)
    assert model.url == url