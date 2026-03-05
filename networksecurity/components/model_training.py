import os, sys
import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier)
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.utils.main_utils.utils import save_pickle_object, load_numpy_array, load_pickle_object
from networksecurity.utils.ml_utils.classification_metrics import get_classification_score, evaluate_model
from networksecurity.utils.ml_utils.network_model import NetworkModel
from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging


class ModelTrainer:
    def __init__(self, transformation_artifact: DataTransformationArtifact, trainer_config: ModelTrainerConfig):
        self.model_input = transformation_artifact
        self.model_config = trainer_config
    
    def train_evaluate_model(self, X_train, X_test, y_train, y_test):
      model_report:dict = evaluate_model(X_train, X_test, y_train, y_test)
      
      best_model_accuracy = max(sorted(list(model_report.values())))
      best_model = list(model_report.keys())[list(model_report.values()).index(best_model_accuracy)]

      y_train_pred = best_model.predict(X_train)
      clasification_train_metric = get_classification_score(y_train, y_train_pred)
      
      y_test_pred = best_model.predict(X_test)
      classification_test_metric = get_classification_score(y_test, y_test_pred)

    
    def initiate_model_training(self)->ModelTrainerArtifact:
        train_arr = load_numpy_array(self.model_input.transformed_train_path)
        test_arr = load_numpy_array(self.model_input.transformed_test_path)
        preprocessor = load_pickle_object(self.model_input.preprocessor_path)

        X_train, X_test, y_train, y_test = (
            train_arr[:, :-1],
            test_arr[:, :-1],
            train_arr[:, -1],
            test_arr[:, -1]
        )



