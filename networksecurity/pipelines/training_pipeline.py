import sys

from networksecurity.constant import training_config
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTranformation
from networksecurity.components.model_training import ModelTrainer
from networksecurity.cloud.s3_syncer import S3_Sync

from networksecurity.entity.config_entity import (TrainingConfig,DataIngestionConfig,
                                                  DataValidationConfig,
                                                  DataTransformationConfig,
                                                  ModelTrainerConfig)
from networksecurity.entity.artifact_entity import (DataIngestionArtifact,
                                                  DataValidationArtifact,
                                                  DataTransformationArtifact,
                                                  ClassificationMetricArtifact,
                                                  ModelTrainerArtifact)

from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingConfig()
        self.s3_sync = S3_Sync()
    def start_data_ingestion(self):
        try:
            logging.info("Initiating Data Ingestion Configuration.")
            self.ingestion_config = DataIngestionConfig(training_par_config=self.training_pipeline_config)
            ingestion_obj = DataIngestion(self.ingestion_config)
            ingestion_artifact = ingestion_obj.initiate_data_ingestion()
            logging.info("Ingestion Completed.")
            return ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_validation(self, ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info("Data Validation Initiated.")
            self.validation_config = DataValidationConfig(self.training_pipeline_config)
            validation_obj = DataValidation(data_validation_config=self.validation_config,
                                            data_ingestion_artifact=ingestion_artifact)
            validation_artifact = validation_obj.initiate_data_validation()
            logging.info("Data Validation Completed.")
            return validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, validation_artifact:DataValidationArtifact):
        try:
            logging.info("Data Transformation Inititated.")
            self.transformation_config = DataTransformationConfig(self.training_pipeline_config)
            transformation_obj = DataTranformation(validation_artifact=validation_artifact,
                                                transformation_config=self.transformation_config)
            transformation_artifact = transformation_obj.initiate_transformation()
            logging.info("Data transformation Completed.")
            return transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_model_training(self, transformation_artifact:DataTransformationArtifact):
        try:
            logging.info("Model Training Initiated.")
            self.model_training_config = ModelTrainerConfig(self.training_pipeline_config)
            model_training_obj = ModelTrainer(trainer_config=self.model_training_config,
                                            transformation_artifact=transformation_artifact)
            model_trainer_artifact = model_training_obj.initiate_model_training()
            logging.info("Model Trained.")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def s3_artifact_syncer(self):
        try:
            aws_bucket_url = f"s3://{training_config.TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(bucket_url=aws_bucket_url, folder=self.training_pipeline_config.artifact_dir)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def s3_model_syncer(self):
        try:
            aws_bucket_url = f"s3://{training_config.TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(bucket_url=aws_bucket_url, folder=self.training_pipeline_config.model_directory)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def run_pipeline(self):
        try:
            logging.info("Starting Pipeline")
            ingestion_artifact = self.start_data_ingestion()
            validation_artifact = self.start_data_validation(ingestion_artifact)
            transformation_artifact = self.start_data_transformation(validation_artifact)
            model_trainer_artifact = self.start_model_training(transformation_artifact)
            logging.info("Pipeline Finished")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)