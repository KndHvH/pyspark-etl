import pytest
from unittest.mock import patch, MagicMock
from service.orms import APIService, PostgresService
from models.connection_models import APIConnectionModel, PostgresConnectionModel
import os
from dotenv import load_dotenv

load_dotenv()

def test_read_api_mock():
    connection_model = APIConnectionModel(url=os.getenv("API_URL"))
    api_service = APIService(connectionModel=connection_model)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"key": "value"}]

    with patch('requests.get', return_value=mock_response):
        result = api_service.read_api()
        assert connection_model.url == os.getenv("API_URL")
        assert result == [{"key": "value"}]
        assert result[0]["key"] == "value"

def test_read_api():
    connection_model = APIConnectionModel(url=os.getenv("API_URL"))
    api_service = APIService(connectionModel=connection_model)

    result = api_service.read_api()
    
    assert connection_model.url == os.getenv("API_URL")
    assert result is not None
    assert len(result) > 0
    assert type(result) == list
    assert type(result[0]) == dict
    assert "name" in result[0]
    assert "common" in result[0]["name"]
