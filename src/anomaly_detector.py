import pandas as pd
from sklearn.ensemble import IsolationForest

# Store fitted models per sensor
_models = {}

def fit(df: pd.DataFrame, sensor_id: str) -> None:
    """
    Fits an Isolation Forest model on the provided data for a specific sensor.
    Assumes the input data is mostly normal behavior.
    """
    sensor_data = df[df['sensor_id'] == sensor_id]
    if sensor_data.empty:
        return

    X = sensor_data[['value']].values

    # Initialize and fit the model
    # contamination is the proportion of outliers in the data set
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(X)

    # Store the model
    _models[sensor_id] = model

def predict(df: pd.DataFrame, sensor_id: str) -> pd.DataFrame:
    """
    Predicts anomalies on the provided data for a specific sensor using the fitted model.
    Adds 'is_anomaly' (bool) and 'anomaly_score' (float) columns.
    """
    if sensor_id not in _models:
        raise ValueError(f"Model for sensor '{sensor_id}' has not been fitted yet.")

    sensor_data = df[df['sensor_id'] == sensor_id].copy()
    if sensor_data.empty:
        # Return empty dataframe with correct columns if no data
        sensor_data['is_anomaly'] = pd.Series(dtype=bool)
        sensor_data['anomaly_score'] = pd.Series(dtype=float)
        return sensor_data

    X = sensor_data[['value']].values
    model = _models[sensor_id]

    # Predict (-1 for anomaly, 1 for normal)
    predictions = model.predict(X)

    # Anomaly score (lower, negative values indicate higher anomaly)
    # We negate it so higher positive value means more anomalous
    scores = -model.score_samples(X)

    sensor_data['is_anomaly'] = predictions == -1
    sensor_data['anomaly_score'] = scores

    return sensor_data
