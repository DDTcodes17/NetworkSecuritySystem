import os, sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
import pickle

from networksecurity.constant.training_config import DATA_TRANSFORMATION_IMPUTER_PARAMS, TARGET_VARIABLE
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.utils.main_utils.utils import save_numpy_array, save_pickle_object
from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging

class DataTranformation:
    def __init__(self, validation_artifact: DataValidationArtifact, transformation_config: DataTransformationConfig):
        self.validation_artifact = validation_artifact
        self.transformation_config = transformation_config
    
    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def get_preprocessor(self)->Pipeline:
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor = Pipeline([("imputer", imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_transformation(self)->DataTransformationArtifact:
        logging.info("Data Transformation Initiated")
        train_df = DataTranformation.read_data(self.validation_artifact.valid_train_path)
        test_df = DataTranformation.read_data(self.validation_artifact.valid_test_path)

        logging.info("Segregating Data into Input and target")
        #Train
        X_train_df = train_df.drop([TARGET_VARIABLE], axis=1)
        y_train = train_df[TARGET_VARIABLE]
        y_train = y_train.replace(-1,0)

        #Test
        X_test_df = test_df.drop([TARGET_VARIABLE], axis=1)
        y_test = test_df[TARGET_VARIABLE]
        y_test = y_test.replace(-1,0)

        logging.info("Performing KNN Imputation as a Pipeline")
        preprocessor = self.get_preprocessor()
        X_transformed_train_df = preprocessor.fit_transform(X_train_df)
        X_transformed_test_df = preprocessor.transform(X_test_df)
        logging.info("Preprocessing Imputation Completed")

        logging.info("Creating and saving numpy arrays and preprocessor files")
        train_arr = np.c_[X_transformed_train_df, np.array(y_train)]
        test_arr = np.c_[X_transformed_test_df, np.array(y_test)]
        
        save_numpy_array(file_path=self.transformation_config.transformed_train_path, array=train_arr)
        save_numpy_array(file_path=self.transformation_config.transformed_test_path, array=test_arr)
        save_pickle_object(file_path=self.transformation_config.data_preprocessor_path, obj=preprocessor)
        
        logging.info("Preprocessor Pusher")
        save_pickle_object("final_model/preprocessor.pkl", preprocessor)
        logging.info("Returning artifacts")
        data_transformation_artifact = DataTransformationArtifact(
            transformed_train_path=self.transformation_config.transformed_train_path,
            transformed_test_path= self.transformation_config.transformed_test_path,
            preprocessor_path=self.transformation_config.data_preprocessor_path
        )
        return data_transformation_artifact
        logging.info("Data Transformation Completed")
