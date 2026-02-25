from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:              # Output of DataIngestion 
    train_file_path:str
    test_file_path:str