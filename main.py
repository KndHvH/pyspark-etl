import logging
import os
from dotenv import load_dotenv
from service.orms import *
from models.connection_models import *
from service.etl_flow import EtlFlow

load_dotenv()

logging.basicConfig(
    filename='logs/etl.log',
    filemode='a',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    
    
    api_service = APIService(
        connectionModel=APIConnectionModel(
            url=os.getenv("API_URL")
        )
    )
    
    
    postgres_service = PostgresService(
        connectionModel=PostgresConnectionModel(
            host=os.getenv("PG_HOST"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASS"),
            database=os.getenv("PG_DB")
        )
    )
    
    etlflow = EtlFlow(services={'source': api_service, 'target': postgres_service})
    etlflow.run()

if __name__ == '__main__':
    try:
        logging.info("Iniciando Processo de ETL")
        main()
    except Exception as e:
        logging.error(f"Erro na execução do Processo: {e}")