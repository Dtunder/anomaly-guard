import pytest
import pandas as pd
from src.sensor_simulator import generate_batch
import src.anomaly_detector as ad

def test_anomaly_detector_detects_injected_anomalies():
    sensor_id = "sensor_1"

    # 1. Fit the model on normal data
    clean_data = generate_batch(n_sensors=1, n_samples=500, anomaly_rate=0.0)
    ad.fit(clean_data, sensor_id)

    # 2. Predict on data with high anomaly rate
    test_data = generate_batch(n_sensors=1, n_samples=200, anomaly_rate=0.1)
    # Make sure we actually have injected anomalies
    injected_count = test_data['is_injected_anomaly'].sum()
    if injected_count == 0:
        pytest.skip("No anomalies randomly injected, skipping test")

    result_df = ad.predict(test_data, sensor_id)

    # Check if 'is_anomaly' and 'anomaly_score' are added
    assert 'is_anomaly' in result_df.columns
    assert 'anomaly_score' in result_df.columns

    # Check detection rate (True Positives / Actual Positives)
    actual_anomalies = result_df[result_df['is_injected_anomaly'] == True]
    detected_anomalies = actual_anomalies[actual_anomalies['is_anomaly'] == True]

    detection_rate = len(detected_anomalies) / len(actual_anomalies)

    # Our simple rule is a +/- 5 std dev, isolation forest should easily catch > 80%
    assert detection_rate >= 0.8, f"Detection rate {detection_rate} is less than 0.8"

def test_predict_before_fit_raises_error():
    sensor_id = "sensor_999"
    test_data = generate_batch(n_sensors=1, n_samples=10, anomaly_rate=0)
    with pytest.raises(ValueError, match="Model for sensor 'sensor_999' has not been fitted yet."):
        ad.predict(test_data, sensor_id)
