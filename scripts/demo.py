import os
import sys

# Ensure src can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.sensor_simulator import generate_batch
import src.anomaly_detector as ad
from src.alert_manager import check_and_alert

def run_demo():
    print("Starting AnomalyGuard end-to-end demo...")

    n_sensors = 3
    sensor_ids = [f"sensor_{i+1}" for i in range(n_sensors)]

    print("\n1. Generating clean baseline data...")
    clean_data = generate_batch(n_sensors=n_sensors, n_samples=300, anomaly_rate=0.0)
    print(f"Generated {len(clean_data)} baseline samples.")

    print("\n2. Fitting models...")
    for sensor_id in sensor_ids:
        ad.fit(clean_data, sensor_id)
        print(f"Fitted model for {sensor_id}.")

    print("\n3. Generating test data with anomalies...")
    test_data = generate_batch(n_sensors=n_sensors, n_samples=100, anomaly_rate=0.05)
    print(f"Generated {len(test_data)} test samples.")

    print("\n4. Predicting anomalies...")
    predicted_data_list = []
    for sensor_id in sensor_ids:
        sensor_data = test_data[test_data['sensor_id'] == sensor_id]
        if not sensor_data.empty:
            pred_df = ad.predict(sensor_data, sensor_id)
            predicted_data_list.append(pred_df)

    processed_data = pd.concat(predicted_data_list)
    anomalies_detected = processed_data['is_anomaly'].sum()
    print(f"Detected {anomalies_detected} anomalies out of {len(processed_data)} samples.")

    print("\n5. Checking for alerts...")
    alerts = check_and_alert(processed_data)
    print(f"Generated {len(alerts)} alerts.")

    if alerts:
        print("\nRecent Alerts:")
        for alert in alerts[:5]:
            print(f"- [{alert['severity']}] {alert['sensor_id']}: {alert['message']}")

        if len(alerts) > 5:
            print(f"... and {len(alerts) - 5} more.")

    print("\nDemo completed successfully.")

if __name__ == "__main__":
    run_demo()
