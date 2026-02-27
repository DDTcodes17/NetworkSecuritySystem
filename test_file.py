from networksecurity.constant.training_config import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file

if __name__== "__main__":
    file = read_yaml_file(SCHEMA_FILE_PATH)
    print(file["numerical_columns"])