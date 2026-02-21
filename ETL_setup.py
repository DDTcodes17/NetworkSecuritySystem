import os
import sys
import pandas as pd
import numpy as np
import certifi
import json
import pymongo
from dotenv import load_dotenv
from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging

ca = certifi.where() #Certification Authority
load_dotenv()
MONGODB_url = os.getenv("MONGO_DB_URL")

class Data_ETL:
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGODB_url)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path).reset_index(drop=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def load_data_mongodb(self,db_name, records, collection_name):
        try:
            self.database = self.mongo_client[db_name]
            self.collection = self.database[collection_name]
            result = self.collection.insert_many(records)
            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data\phisingData.csv"
    db_name = "Dhruv_Cyber"
    collection_name = "NetworkData"
    
    network_obj = Data_ETL()
    records = network_obj.csv_to_json_converter(FILE_PATH)
    print(records[0])
    no_of_records=network_obj.load_data_mongodb(records=records, db_name=db_name, collection_name=collection_name)
    print(no_of_records)
        