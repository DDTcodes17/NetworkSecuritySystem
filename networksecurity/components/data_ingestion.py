import os
import sys
import numpy as np
import pandas as pd
import pymongo
from dataclasses import dataclass
from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

load_dotenv()
MONGODB_url = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def convert_to_dataframe(self):
        database_name = self.data_ingestion_config.database_name
        collection_name = self.data_ingestion_config.collection_name
        self.mongo_client = pymongo.MongoClient(MONGODB_url)
        collection = self.mongo_client[database_name][collection_name]

        df = pd.DataFrame(collection.find())
        if "_id" in df.columns.to_list():
            df = df.drop("_id", axis=1)
        df = df.replace({"na":np.nan})
        return df
    
    def import_to_feature_store(self, df: pd.DataFrame):
        try:
            feature_store_path = self.data_ingestion_config.feature_store_path
            dir_path = os.path.dirname(feature_store_path)
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_path, index=False, header=True)
            logging.info("Raw Data Imported")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def train_test_split(self, df: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=1234)
            logging.info("Train Test Split Initiated")

            ingested_path = os.path.dirname(self.data_ingestion_config.train_path)
            os.makedirs(ingested_path)
            logging.info("Importing Training and testing data")

            train_set.to_csv(self.data_ingestion_config.train_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_path, index=False, header=True)

            logging.info("Import Successful")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_ingestion(self):
        try:
            df = self.convert_to_dataframe()
            self.import_to_feature_store(df=df)
            self.train_test_split(df=df)
            ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.train_path,
                                                    test_file_path=self.data_ingestion_config.test_path)
            return ingestion_artifact
            logging.info("Data Ingestion Completed")
        except Exception as e:
            raise NetworkSecurityException(e, sys)    

