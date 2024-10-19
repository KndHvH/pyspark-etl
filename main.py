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
            host=os.getenv("POSTGRES_HOST"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASS"),
            database=os.getenv("POSTGRES_DB")
        )
    )
    
    etlflow = EtlFlow(services={'source': sap_hana_service, 'target': sql_server_service})
    etlflow.run()

if __name__ == '__main__':
    try:
        logging.info("Iniciando Processo de ETL")
        main()
    except Exception as e:
        logging.error(f"Erro na execução do Processo: {e}")