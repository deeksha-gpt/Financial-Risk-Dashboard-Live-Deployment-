import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


class MLAnomalyDetector:
    """ML-based anomaly detection for risk metrics."""

    def __init__(self, contamination=0.1):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42
        )
        self.is_fitted = False

    def train(self, historical_metrics: pd.DataFrame):
        """Train anomaly detection model on historical metrics."""

        features = historical_metrics[['var', 'delta', 'gamma', 'vega']].values
        self.model.fit(features)

        self.is_fitted = True

    def detect_anomaly(self, current_metrics: dict) -> bool:
        """Detect if current metrics are anomalous."""

        if not self.is_fitted:
            raise ValueError("Model not trained")

        features = np.array([[
            current_metrics['var'],
            current_metrics['delta'],
            current_metrics['gamma'],
            current_metrics['vega']
        ]])

        prediction = self.model.predict(features)

        return prediction[0] == -1
    
    import torch
import torch.nn as nn


class VaRPredictor(nn.Module):
    """LSTM model to predict next-day VaR."""

    def __init__(self, input_size=10, hidden_size=50, num_layers=2):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True
        )

        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):

        out, _ = self.lstm(x)

        out = self.fc(out[:, -1, :])

        return out
    
