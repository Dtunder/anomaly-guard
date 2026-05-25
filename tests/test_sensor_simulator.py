import pytest
import pandas as pd
from src.sensor_simulator import generate_batch

def test_generate_batch_shape_and_columns():
    n_sensors = 2
    n_samples = 50
    df = generate_batch(n_sensors=n_sensors, n_samples=n_samples)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == n_sensors * n_samples

    expected_cols = ['timestamp', 'sensor_id', 'value', 'unit', 'is_injected_anomaly']
    for col in expected_cols:
        assert col in df.columns

def test_generate_batch_anomalies_present():
    # With a high anomaly rate, we should see at least one anomaly
    df = generate_batch(n_sensors=1, n_samples=1000, anomaly_rate=0.5)
    assert df['is_injected_anomaly'].sum() > 0

def test_sensor_units():
    df = generate_batch(n_sensors=4, n_samples=10, anomaly_rate=0)
    units = df['unit'].unique()
    assert set(units) == {"C", "mm/s", "bar", "RPM"}
