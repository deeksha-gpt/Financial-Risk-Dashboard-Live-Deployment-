from sklearn.ensemble import IsolationForest
import numpy as np

class MLAnomalyDetector:

    def __init__(self):
        self.model = IsolationForest()

    def detect(self, data):
        return self.model.predict(data)