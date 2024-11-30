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
            df = pd.read_csv(file_path)
            df = df.dropna()
            df = df.drop_duplicates()
            df = df.reset_index(drop=True)
            df = df.to_dict(orient='records')
            return df
        except Exception as e:
            error = NetworkSecurityException(e, sys)
            logging.error(error.error_message)
            raise error