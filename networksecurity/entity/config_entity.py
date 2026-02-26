#Abstraction of all Inputs and Outputs
import os
from datetime import datetime

from networksecurity.constant import training_config

print(training_config.ARTIFACT_FILENAME)
print(training_config.PIPELINE_NAME)

class TrainingConfig:
    def __init__(self, timestamp = datetime.now()):
        timestamp = timestamp.strftime("%d_%m_%Y_%H_%M_%S")
        self.pipeline_name = training_config.PIPELINE_NAME
        self.artifact_name = training_config.ARTIFACT_FILENAME
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)

class DataIngestionConfig:
    def __init__(self, training_par_config: TrainingConfig):
        self.data_ingestion_dir = os.path.join(training_par_config.artifact_dir, training_config.DATA_INGESTION_DIRECTORY)
        self.feature_store_path = os.path.join(self.data_ingestion_dir, training_config.DATA_INGESTION_FEATURE_STORE, training_config.DATA_FILE)
        self.train_path = os.path.join(self.data_ingestion_dir, training_config.DATA_INGESTION_INGESTED_STORE, training_config.TRAIN_FILE_NAME)
        self.test_path = os.path.join(self.data_ingestion_dir, training_config.DATA_INGESTION_INGESTED_STORE, training_config.TEST_FILE_NAME)
        # We already have .csv format raw data file
        self.train_test_split_ratio = training_config.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO 
        self.collection_name = training_config.DATA_INGESTION_COLLECTION_NAME
        self.database_name = training_config.DATA_INGESTION_DATABASE_NAME

#Data Validation: Validating Features, feature distribution, data drift
class DataValidationConfig:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        self.train_path = os.path.join(data_ingestion_config.train_path)
        self.test_path = os.path.join(data_ingestion_config.test_path)
        
        self.validation_dir_path = os.path.join(training_config.DATA_VALIDATION_DIR)
        self.validated_path = os.path.join(self.validation_dir_path, training_config.DATA_VALIDATION_VALID_DIR)
        self.invalid_path = os.path.join(self.validation_dir_path, training_config.DATA_VALIDATION_INVALID_DIR)
        self.data_drift_report_path = os.path.join(self.validation_dir_path, training_config.DATA_VALIDATION_DRIFT_REPORT_DIR, training_config.DATA_VALIDATION_DRIFT_REPORT)
