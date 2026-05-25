import pandas as pd
from typing import List, Dict

# In-memory store for alerts
_alert_log: List[Dict] = []

def check_and_alert(df: pd.DataFrame) -> List[Dict]:
    """
    Checks the dataframe for anomalies and returns a list of new alerts.
    Dataframe must contain 'is_anomaly' and 'anomaly_score' columns.
    """
    new_alerts = []

    if 'is_anomaly' not in df.columns or 'anomaly_score' not in df.columns:
        return new_alerts

    anomalies = df[df['is_anomaly'] == True]

    for _, row in anomalies.iterrows():
        # Determine severity based on anomaly score
        # These thresholds are arbitrary for the MVP
        score = row['anomaly_score']

        # Scikit-learn isolation forest score_samples gives negative values
        # But we negated them in anomaly_detector, so they are positive now.
        # Let's say baseline normal score is around 0.3-0.5.
        # Anomalies might have scores > 0.6.
        if score > 0.8:
            severity = "HIGH"
        elif score > 0.6:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        alert = {
            "timestamp": row['timestamp'],
            "sensor_id": row['sensor_id'],
            "value": row['value'],
            "unit": row['unit'],
            "anomaly_score": float(score),
            "severity": severity,
            "message": f"Anomaly detected on {row['sensor_id']}: {row['value']:.2f} {row['unit']} (Severity: {severity})"
        }

        new_alerts.append(alert)
        _alert_log.append(alert)

    return new_alerts

def get_all_alerts() -> List[Dict]:
    """Returns all recorded alerts."""
    return _alert_log.copy()

def clear_alerts() -> None:
    """Clears the in-memory alert log."""
    _alert_log.clear()
