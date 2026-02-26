from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:              # Output of DataIngestion 
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:             #Output of DataValidation
    validation_status: bool
    valid_train_path:str
    valid_test_path: str
    invalid_train_path:str
    invalid_test_path:str
    data_drift_report:str
