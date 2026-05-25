# AnomalyGuard MVP

Real-time Machine Anomaly Detection for Industrial SMEs (KMUs).

## Overview
AnomalyGuard MVP provides a lightweight, real-time machine anomaly detection dashboard.
It uses a synthetic sensor data generator simulating real-world manufacturing conditions with injected anomalies.
The core detection engine is powered by an `IsolationForest` model, providing high accuracy with minimal configuration.
The MVP includes an interactive Streamlit dashboard for real-time visualization and alerting.

## Key Features
*   **Real-time Dashboard**: Streamlit-based UI with live updating Plotly charts visualizing machine data.
*   **Anomaly Detection**: Scikit-learn's `IsolationForest` wrapper fitting on normal baseline data and predicting anomalies in real time.
*   **Sensor Simulation**: Injects realistic noise and significant anomalies across multiple simulated sensors (Temperature, Vibration, Pressure, RPM).
*   **Alert Management**: In-memory tracking of anomalies with dynamic severity classification (LOW, MEDIUM, HIGH) based on anomaly scores.

## Installation
1. Clone the repository.
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application
```bash
streamlit run app.py
```

## Running Tests
```bash
PYTHONPATH=. pytest tests/
```
