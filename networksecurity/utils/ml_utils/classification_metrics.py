import os, sys
from sklearn.metrics import f1_score, precision_score, recall_score

from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exceptions.exceptions import NetworkSecurityException

class ClassificationMetrics:
    def __init__(self, y_true, y_pred):
        self.y_true = y_true
        self.y_pred = y_pred
    
    def get_classification_score(self)->ClassificationMetricArtifact:
        try:
            model_f1 = f1_score(self.y_true, self.y_pred)
            model_precision = precision_score(self.y_true, self.y_pred)
            model_recall = recall_score(self.y_true, self.y_pred)

            return ClassificationMetricArtifact(
                f1_score=model_f1,
                precision=model_precision,
                recall=model_recall
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)