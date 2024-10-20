import time
import requests
import pandas as pd
from datetime import datetime, timedelta
from models.connection_models import APIConnectionModel, PostgresConnectionModel
from sqlalchemy import create_engine

class APIService():
    def __init__(self, connectionModel: APIConnectionModel):
        self._connectionModel = connectionModel
    
    def read_api(self) -> pd.DataFrame:
        payload = self._fetch_data(url=self._connectionModel.url)
        return payload          
    
    def _fetch_data(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Erro na requisição: {response.status_code}")
        return response.json()

class PostgresService():
    def __init__(self, connectionModel:PostgresConnectionModel):
        self._connectionModel = connectionModel
        self._engine = create_engine(f'postgresql://{self._connectionModel.user}:{self._connectionModel.password}@{self._connectionModel.host}/{self._connectionModel.database}')
    
    def execute_query(self, query):
        with self._engine.connect() as connection:
            result = connection.execute(query)
            return result.fetchall()
    
    def read_sql(self, query):
        with self._engine.connect() as connection:
            return pd.read_sql(query, connection)
    
    def insert_data_to_sql(self, df, table, if_exists='append', index=False):
        df.to_sql(table, self._engine, if_exists=if_exists, index=index)
