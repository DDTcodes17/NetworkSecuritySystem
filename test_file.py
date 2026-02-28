from networksecurity.constant.training_config import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.config_entity import TrainingConfig
import os

if __name__== "__main__":
    file = read_yaml_file(SCHEMA_FILE_PATH)
    print(len(file['columns']))
    # training_obj = TrainingConfig()
    # valid_obj = DataValidationConfig(training_par_config=training_obj)
    # print(os.path.join(valid_obj.data_drift_report_path))
    # print(os.path.dirname(valid_obj.data_drift_report_path))