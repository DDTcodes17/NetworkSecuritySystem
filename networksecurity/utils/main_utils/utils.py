import yaml
import dill
import pickle
import os, sys
import numpy as np
from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

def write_yaml_file(file_path:str, content:object, replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array(file_path:str, array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file:
            np.save(file, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_pickle_object(file_path:str, obj:object):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def load_pickle_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"{file_path} missing. Please Crosscheck.")
        else:
            with open(file_path, "rb") as file:
                print(file)
                return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_numpy_array(file_path)->np.array:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"{file_path} missing. Please Crosscheck.")
        else:
            with open(file_path, "rb") as file:
                return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)