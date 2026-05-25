import pytest
import pandas as pd
from datetime import datetime
from src.alert_manager import check_and_alert, get_all_alerts, clear_alerts

def test_check_and_alert_appends_to_log():
    clear_alerts()

    # Create mock dataframe with anomalies
    df = pd.DataFrame({
        'timestamp': [datetime.now(), datetime.now()],
        'sensor_id': ['sensor_1', 'sensor_2'],
        'value': [100.0, 200.0],
        'unit': ['C', 'RPM'],
        'is_anomaly': [True, False], # Only one anomaly
        'anomaly_score': [0.9, 0.1]
    })

    new_alerts = check_and_alert(df)

    assert len(new_alerts) == 1
    assert new_alerts[0]['sensor_id'] == 'sensor_1'
    assert new_alerts[0]['severity'] == 'HIGH'

    all_alerts = get_all_alerts()
    assert len(all_alerts) == 1
    assert all_alerts[0] == new_alerts[0]

def test_check_and_alert_severity_classification():
    clear_alerts()

    df = pd.DataFrame({
        'timestamp': [datetime.now(), datetime.now(), datetime.now()],
        'sensor_id': ['sensor_1', 'sensor_1', 'sensor_1'],
        'value': [100.0, 100.0, 100.0],
        'unit': ['C', 'C', 'C'],
        'is_anomaly': [True, True, True],
        'anomaly_score': [0.9, 0.7, 0.5]
    })

    new_alerts = check_and_alert(df)

    assert len(new_alerts) == 3
    assert new_alerts[0]['severity'] == 'HIGH'
    assert new_alerts[1]['severity'] == 'MEDIUM'
    assert new_alerts[2]['severity'] == 'LOW'

def test_check_and_alert_missing_columns():
    clear_alerts()

    df = pd.DataFrame({
        'timestamp': [datetime.now()],
        'sensor_id': ['sensor_1'],
        'value': [100.0]
    })

    new_alerts = check_and_alert(df)
    assert len(new_alerts) == 0
    assert len(get_all_alerts()) == 0
