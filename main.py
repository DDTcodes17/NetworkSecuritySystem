from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging


if __name__ == "__main__":
    training_par_config = TrainingConfig()
    ingestion_config = DataIngestionConfig(training_par_config=training_par_config)
    ingestion_obj = DataIngestion(data_ingestion_config = ingestion_config)
    ingestion_artifact = ingestion_obj.initiate_data_ingestion()
    logging.info("Data Ingestion Component Successfull")
    print(ingestion_artifact)
    
    print("Now Data Validation")
    validation_config = DataValidationConfig(training_par_config=training_par_config)
    validation_obj = DataValidation(ingestion_artifact,validation_config)
    validation_artifact = validation_obj.initiate_data_validation()
    print(validation_artifact)
    logging.info("Data Validation Component Successful")
    
