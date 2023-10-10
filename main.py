from sensor.configuration.mongo_db_connection import MongoDBClient
#from sensor.exception import SensorException
#rom sensor.logger import logging
from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
import sys,os

if __name__=="__main__":

    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    print(data_ingestion_config.__dict__)
    # try:
    #     logging.info("dividing by zero")
    #     x=1/0
    # except Exception as e:
    #     raise SensorException(e,sys)
        



    #mongo_db_client = MongoDBClient()
    #print("collection name:", mongo_db_client.database.list_collection_names())