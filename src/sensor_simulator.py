import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_batch(n_sensors: int = 3, n_samples: int = 100, anomaly_rate: float = 0.05) -> pd.DataFrame:
    """
    Generates a batch of sensor time-series data with injected anomalies.
    """
    data = []

    # Types of sensors
    sensor_types = [
        {"unit": "C", "base": 50.0, "noise": 2.0},  # Temperature
        {"unit": "mm/s", "base": 5.0, "noise": 0.5}, # Vibration
        {"unit": "bar", "base": 10.0, "noise": 0.5}, # Pressure
        {"unit": "RPM", "base": 1500.0, "noise": 50.0} # RPM
    ]

    # To maintain continuous time across batches if called sequentially,
    # we use a global tracker or just the current time if not provided.
    # We will use datetime.now() as a base but stagger it properly.
    if not hasattr(generate_batch, "last_timestamp"):
        generate_batch.last_timestamp = datetime.now()

    start_time = generate_batch.last_timestamp

    for sensor_idx in range(n_sensors):
        sensor_id = f"sensor_{sensor_idx + 1}"
        s_type = sensor_types[sensor_idx % len(sensor_types)]

        for sample_idx in range(n_samples):
            timestamp = start_time + timedelta(seconds=sample_idx)

            # Normal behavior
            value = np.random.normal(s_type["base"], s_type["noise"])

            # Inject anomaly
            is_anomaly = False
            if np.random.random() < anomaly_rate:
                is_anomaly = True
                # Anomaly is significant deviation (e.g., + or - 5 standard deviations)
                direction = 1 if np.random.random() > 0.5 else -1
                value += direction * 5 * s_type["noise"]

            data.append({
                "timestamp": timestamp,
                "sensor_id": sensor_id,
                "value": value,
                "unit": s_type["unit"],
                "is_injected_anomaly": is_anomaly
            })

    # Update last_timestamp for the next batch
    generate_batch.last_timestamp = start_time + timedelta(seconds=n_samples)

    return pd.DataFrame(data)
