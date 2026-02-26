import yaml
import dill
import pickle
import os, sys
from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e