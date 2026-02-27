#Data Validation: Validating Features, feature distribution, data drift

from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging
from networksecurity.constant.training_config import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
import os, sys
import pandas as pd
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def is_same_num_columns(self, df:pd.DataFrame)->bool:
        num_actual = len(self._schema_config)
        
        if len(df.columns)==num_actual:
            status=True
        else:
            status=False
        return status
    
    def is_numeric_cols_exist(self, df:pd.DataFrame)->bool:
        num_actual = len(self._schema_config['numerical_columns'])
        df_numeric = len([cols for cols in df.columns if df[cols].dtype!='o'])
        if num_actual == df_numeric:
            return True
        else:
            return False
    
    def data_drift_check(self, base_df, current_df, threshold=0.05):
        status = True
        report = {}
        for col in base_df.columns:
            dist_1 = base_df[col]
            dist_2 = current_df[col]
            dist_check = ks_2samp(dist_1, dist_2)

            if dist_check.pvalue >=threshold:
                is_found=False
            else:
                is_found=True
                status=False
            report.update({col:
                           {"dist_check": dist_check.pvalue,
                            "is_found":is_found }})
            #writing into drift file
        drift_report_path = self.data_validation_config.data_drift_report_path
        dir_path=os.path.dirname(drift_report_path)
        os.makedirs(dir_path, exist_ok=True)
        write_yaml_file(file_path=drift_report_path, content=report)

    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            logging.info("Beginning Data Validation: Number_of_columns")

            train_status = DataValidation.is_same_num_columns(train_df)
            if not train_status:
                print("Train Validation not successful")
            test_status = DataValidation.is_same_num_columns(test_df)
            if not test_status:
                print("Test validation not successful")
            logging.info("No. of Columns Validation successful on both train and test")

            logging.info("Numeric Columns exist Validation begin")
            numeric_status_train = DataValidation.is_numeric_cols_exist(train_df)
            if not numeric_status_train:
                print("Different numeric columns found in Train set")
            numeric_status_test = DataValidation.is_numeric_cols_exist(test_df)
            if not numeric_status_test:
                print("Different numeric columns found in Test set")
            logging.info("Numeric Column Validation ends")

            logging.info("Data Drift Validation begins")

        except Exception as e:
            raise NetworkSecurityException(e, sys)