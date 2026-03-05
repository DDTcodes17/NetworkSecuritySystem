import os, sys
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier)
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exceptions.exceptions import NetworkSecurityException


def get_classification_score(y_true, y_pred)->ClassificationMetricArtifact:
    try:
        model_f1 = f1_score(y_true, y_pred)
        model_precision = precision_score(y_true, y_pred)
        model_recall = recall_score(y_true, y_pred)

        return ClassificationMetricArtifact(
            f1_score=model_f1,
            precision=model_precision,
            recall=model_recall
        )
    except Exception as e:
            raise NetworkSecurityException(e, sys)

def evaluate_model(X_train, X_test, y_train, y_test):
        try:
            models = {
                "Logistic Regression": LogisticRegression(),
                "KNN": KNeighborsClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "XGBoost": XGBClassifier()
                }

            params={
                "Logistic Regression":{},
                "KNN":{
                    "n_neighbors":[4,5,6]
                },
                "Decision Tree":{
                    "criterion":["gini", "entropy", "log_loss"]
                },
                "Random Forest":{
                    "n_estimators":[8,16,32,64,128]
                },
                "Gradient Boosting":{
                    "learning_rate": [0.01, 0.1, 0.5]
                },
                "XGBoost": {
                    "eta":[ 0.2, 0.5],
                    "max_depth": [5,6]
                }
            }
            report = {}
            for i in range(len(list(models))):
                model = list(models.values())[i]
                param = list(params.values())[i]
                gs = GridSearchCV(model, param_grid=param, cv=3)
                gs.fit(X_train, y_train)
                model.set_params(**gs.best_params_)
                model.fit(X_train, y_train)

                y_test_pred = model.predict(X_test)
                test_accuracy = accuracy_score(y_true=y_test, y_pred=y_test_pred)
                report[list(models.keys())[i]] = test_accuracy
            return report
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)    
            