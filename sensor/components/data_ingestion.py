from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData
from pandas import DataFrame


class DataIngestion:

    def __init__(self, data_ingestion_config = DataIngestionConfig):
        self.data_ingestion_config = DataIngestionConfig()

    # def initiate_data_ingestion(self)-> DataIngestionArtifact:
    #     try:
    #         pass
    #     except Exception as e:
    #         raise SensorException(e,sys)
        
    def export_data_into_feature_store(self)-> DataFrame:
        """
        Export mongo db collection record as data frame into feature
        """
        try:
            logging.info("Exporting data from mongodb to feature store")
            sensor_data = SensorData()
            sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            #creating folder for feature store
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(feature_store_file_path,exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            return dataframe
            
        except Exception as e:
            raise SensorException(e,sys)

