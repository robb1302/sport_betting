
from sklearn.metrics import precision_score
from typing import List
from pytorch_tabnet.metrics import Metric
from sklearn.metrics import roc_auc_score

class Precision(Metric):
    def __init__(self):
        self._name = "precision"
        self._maximize = True

    def __call__(self, y_true: List[int], y_pred: List[int]):
        precision = precision_score(y_true, y_pred[:,1]>0.5)
        return precision

class Gini(Metric):
    def __init__(self):
        self._name = "gini"
        self._maximize = True

    def __call__(self, y_true, y_score):
        auc = roc_auc_score(y_true, y_score[:, 1])
        return max(2*auc - 1, 0.)