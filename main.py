from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging


if __name__ == "__main__":
    training_par_config = TrainingConfig()
    ingestion_config = DataIngestionConfig(training_par_config=training_par_config)
    ingestion_obj = DataIngestion(data_ingestion_config = ingestion_config)
    ingestion_artifact = ingestion_obj.initiate_data_ingestion()
    logging.info("Data Ingestion Component Successfull")
    print(ingestion_artifact)