import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()

ca = certifi.where()


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            error = NetworkSecurityException(e, sys)
            logging.error(error.error_message)
            raise error
        
    def cv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            error = NetworkSecurityException(e, sys)
            logging.error(error.error_message)
            raise error
        
    def insert_data_to_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(os.getenv("MONGO_DB_URL"), tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            return len(self.records)

        except Exception as e:
            error = NetworkSecurityException(e, sys)
            logging.error(error.error_message)
            raise error
        
if __name__ == "__main__":
    DATA_FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "asad_db"
    COLLECTION = "netwrok_phising_data"

    data_extract = NetworkDataExtract()
    records = data_extract.cv_to_json_convertor(file_path = DATA_FILE_PATH)
    print(records)
    no_of_records = data_extract.insert_data_to_mongodb(records = records, database= DATABASE, collection = COLLECTION)
    print(no_of_records)

