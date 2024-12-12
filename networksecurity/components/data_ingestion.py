import os 
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Configuration of the Data Ingestion 
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    # ------------------------------------------------
    def export_collection_as_dataframe(self):
        """
        This method just reads data from MongoDB and returns a pandas dataframe
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL) 

            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            
            df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)
    # ------------------------------------------------
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # creating folder 
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # ------------------------------------------------
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            logging.info("Performed train test split on the dataframe")
            train_set, test_set = train_test_split(
                dataframe, 
                test_size = self.data_ingestion_config.train_test_split_ratio, 
                )
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_dataset_file_path)   
            os.makedirs(dir_path, exist_ok=True)  

            train_set.to_csv(
                self.data_ingestion_config.train_dataset_path, 
                index=False, 
                header=True)
            test_set.to_csv(
                self.data_ingestion_config.test_dataset_path, 
                index=False, 
                header=True)

            logging.info("Exported train and test files at path")
            logging.info("Exited split_data_as_train_test method of DataIngestion class")

            return (
                self.data_ingestion_config.train_dataset_path,
                self.data_ingestion_config.test_dataset_path,
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)
            logging.info("Exited split_data_as_train_test method of DataIngestion class")


    # ------------------------------------------------

    def initiate_data_ingestion(self) -> List[str]:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training data
        
        Output      :   The connection string is returned as the method's only output
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered the data_ingestion method of Data_Ingestion class")
        try:
            dataframe = self.export_collection_as_dataframe()

            dataframe = self.export_data_into_feature_store(dataframe)

            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path = self.data_ingestion_config.train_dataset_path,
                test_file_path=self.data_ingestion_config.test_dataset_path,
            )

            logging.info("Exited the initiate_data_ingestion method of Data_Ingestion class")

            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)