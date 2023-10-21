import pymongo
from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variable import MONGODB_URL_KEY
import certifi
import os,sys
from sensor.exception import SensorException
ca = certifi.where()

class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:

            if MongoDBClient.client is None:
                #mongo_db_url = os.getenv(MONGODB_URL_KEY)
                mongo_db_url = "mongodb+srv://mujtaba7794:Jameel1480@cluster0.mkmzuzi.mongodb.net/"
                #print(mongo_db_url)
                # if "localhost" in mongo_db_url:
                #     MongoDBClient.client = pymongo.MongoClient(mongo_db_url) 
                # else:
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise SensorException(e,sys)