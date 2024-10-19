import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from service.orms import APIService, PostgresService
from models.connection_models import APIConnectionModel, PostgresConnectionModel
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.asyncio
async def test_read_api():
    connection_model = APIConnectionModel(url=os.getenv("API_URL"))
    api_service = APIService(connectionModel=connection_model)

    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"key": "value"}

    with patch('aiohttp.ClientSession.get', return_value=mock_response):
        result = await api_service.read_api()
        assert result == {"key": "value"}
        assert connection_model.url == os.getenv("API_URL")

def test_execute_query():
    connection_model = PostgresConnectionModel(
        host=os.getenv("SQLS_HOST"), 
        user=os.getenv("SQLS_USER"), 
        password=os.getenv("SQLS_PASS"), 
        database=os.getenv("SQLS_DB")
    )
    postgres_service = PostgresService(connectionModel=connection_model)

    mock_connection = MagicMock()
    mock_connection.execute.return_value.fetchall.return_value = [("result1",), ("result2",)]

    with patch('sqlalchemy.create_engine') as mock_create_engine:
        mock_create_engine.return_value.connect.return_value.__enter__.return_value = mock_connection
        result = postgres_service.execute_query("SELECT * FROM table")
        assert result == [("result1",), ("result2",)]
        assert connection_model.host == os.getenv("SQLS_HOST")
        assert connection_model.user == os.getenv("SQLS_USER")
        assert connection_model.password == os.getenv("SQLS_PASS")
        assert connection_model.database == os.getenv("SQLS_DB")

def test_read_sql():
    connection_model = PostgresConnectionModel(
        host=os.getenv("SQLS_HOST"), 
        user=os.getenv("SQLS_USER"), 
        password=os.getenv("SQLS_PASS"), 
        database=os.getenv("SQLS_DB")
    )
    postgres_service = PostgresService(connectionModel=connection_model)

    mock_connection = MagicMock()
    mock_df = MagicMock()

    with patch('sqlalchemy.create_engine') as mock_create_engine, \
         patch('pandas.read_sql', return_value=mock_df) as mock_read_sql:
        mock_create_engine.return_value.connect.return_value.__enter__.return_value = mock_connection
        result = postgres_service.read_sql("SELECT * FROM table")
        mock_read_sql.assert_called_once_with("SELECT * FROM table", mock_connection)
        assert result == mock_df
        assert connection_model.host == os.getenv("SQLS_HOST")
        assert connection_model.user == os.getenv("SQLS_USER")
        assert connection_model.password == os.getenv("SQLS_PASS")
        assert connection_model.database == os.getenv("SQLS_DB")
