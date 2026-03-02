import os, sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
import pickle

from networksecurity.constant.training_config import DATA_TRANSFORMATION_IMPUTER_PARAMS, TARGET_VARIABLE
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.utils.main_utils.utils import save_numpy_array, save_pickle_object
from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging

class DataTranformation:
    def __init__(self):
        pass