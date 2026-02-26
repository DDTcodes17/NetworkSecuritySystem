import os
import sys

"""Commom Constants for training"""
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
DATA_FILE: str = "phisingData.csv"

PIPELINE_NAME: str = "NetworkSecurity"
TARGET_VARIABLE: str = "Result"
ARTIFACT_FILENAME: str = "artifact"
SCHEMA_FILE_PATH = os.path.join("schema_file", "schema.yaml")    #Path needed by read_yaml funtion


"""Constants for Data Ingestion"""
DATA_INGESTION_COLLECTION_NAME:str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "Dhruv_Cyber"
DATA_INGESTION_DIRECTORY: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE: str = "feature_store"    # Storing raw data
DATA_INGESTION_INGESTED_STORE: str = "ingested"        # Split data
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: str = 0.2

"""Constants for Data Validation"""
DATA_VALIDATION_DIR:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "valid"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT:str = "report.yaml"