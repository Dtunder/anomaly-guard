import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from src.sensor_simulator import generate_batch
import src.anomaly_detector as ad
from src.alert_manager import check_and_alert

st.set_page_config(page_title="AnomalyGuard MVP", layout="wide")

st.title("AnomalyGuard MVP")
st.subheader("Real-time Machine Anomaly Detection")

# Sidebar for controls
st.sidebar.header("Simulation Controls")
n_sensors = st.sidebar.slider("Number of Sensors", 1, 4, 3)
n_samples = st.sidebar.slider("Samples per Batch", 10, 200, 50)
anomaly_rate = st.sidebar.slider("Anomaly Injection Rate", 0.0, 0.2, 0.05)
update_speed = st.sidebar.slider("Update Speed (seconds)", 0.5, 5.0, 2.0)

# Initialize session state for persistent data
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = pd.DataFrame()
if 'alert_log' not in st.session_state:
    st.session_state.alert_log = []
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'models_fitted' not in st.session_state:
    st.session_state.models_fitted = False
if 'current_n_sensors' not in st.session_state:
    st.session_state.current_n_sensors = n_sensors

# Handle slider changes resetting models
if st.session_state.current_n_sensors != n_sensors:
    st.session_state.models_fitted = False
    st.session_state.current_n_sensors = n_sensors

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Start Simulation"):
        st.session_state.is_running = True
with col2:
    if st.button("Stop Simulation"):
        st.session_state.is_running = False
with col3:
    if st.button("Clear Data"):
        st.session_state.historical_data = pd.DataFrame()
        st.session_state.alert_log = []
        st.session_state.models_fitted = False
        st.rerun()

# Fit models before first prediction
if st.session_state.is_running and not st.session_state.models_fitted:
    with st.spinner("Initializing and fitting models on normal data..."):
        # Generate some clean data to fit
        clean_data = generate_batch(n_sensors=n_sensors, n_samples=300, anomaly_rate=0.0)
        for i in range(n_sensors):
            ad.fit(clean_data, f"sensor_{i+1}")
        st.session_state.models_fitted = True

# Layout
chart_placeholder = st.empty()
st.subheader("Alert Log")
alert_placeholder = st.empty()

def update_dashboard():
    # Generate new batch
    new_data = generate_batch(n_sensors=n_sensors, n_samples=n_samples, anomaly_rate=anomaly_rate)

    # Predict anomalies
    predicted_data_list = []
    for i in range(n_sensors):
        sensor_id = f"sensor_{i+1}"
        sensor_data = new_data[new_data['sensor_id'] == sensor_id]
        if not sensor_data.empty:
            pred_df = ad.predict(sensor_data, sensor_id)
            predicted_data_list.append(pred_df)

    if predicted_data_list:
        processed_data = pd.concat(predicted_data_list)

        # Check and alert
        new_alerts = check_and_alert(processed_data)
        if new_alerts:
            # Reverse to prepend new alerts
            for alert in reversed(new_alerts):
                st.session_state.alert_log.insert(0, alert)

        # Append to historical data (keep last 1000 points to avoid memory issues)
        st.session_state.historical_data = pd.concat([st.session_state.historical_data, processed_data])

        # Keep only the latest 1000 records per sensor
        st.session_state.historical_data = st.session_state.historical_data.groupby('sensor_id').tail(1000).reset_index(drop=True)

        # Plotly chart
        fig = go.Figure()

        for sensor_id in st.session_state.historical_data['sensor_id'].unique():
            sensor_hist = st.session_state.historical_data[st.session_state.historical_data['sensor_id'] == sensor_id]

            # Normal line
            fig.add_trace(go.Scatter(
                x=sensor_hist['timestamp'],
                y=sensor_hist['value'],
                mode='lines',
                name=f"{sensor_id} (Normal)",
                line=dict(width=1)
            ))

            # Anomalies in red
            anomalies = sensor_hist[sensor_hist['is_anomaly'] == True]
            if not anomalies.empty:
                fig.add_trace(go.Scatter(
                    x=anomalies['timestamp'],
                    y=anomalies['value'],
                    mode='markers',
                    name=f"{sensor_id} (Anomaly)",
                    marker=dict(color='red', size=8, symbol='x')
                ))

        fig.update_layout(
            title="Real-time Sensor Data with Detected Anomalies",
            xaxis_title="Time",
            yaxis_title="Value",
            height=500,
            hovermode="x unified"
        )

        chart_placeholder.plotly_chart(fig, use_container_width=True)

        # Alert Table
        if st.session_state.alert_log:
            # Convert to DataFrame for nice rendering
            alert_df = pd.DataFrame(st.session_state.alert_log)
            # Add some color to severity
            def color_severity(val):
                color = 'red' if val == 'HIGH' else 'orange' if val == 'MEDIUM' else 'yellow'
                return f'color: {color}'

            # Format display
            display_df = alert_df[['timestamp', 'sensor_id', 'severity', 'message']].copy()
            # Sort by timestamp descending
            display_df = display_df.sort_values(by='timestamp', ascending=False).head(50) # Show last 50

            alert_placeholder.dataframe(
                display_df.style.map(color_severity, subset=['severity']),
                use_container_width=True,
                hide_index=True
            )

# Main loop
if st.session_state.is_running and st.session_state.models_fitted:
    update_dashboard()
    time.sleep(update_speed)
    st.rerun()
elif not st.session_state.is_running and not st.session_state.historical_data.empty:
    # Just render the existing data
    fig = go.Figure()
    for sensor_id in st.session_state.historical_data['sensor_id'].unique():
        sensor_hist = st.session_state.historical_data[st.session_state.historical_data['sensor_id'] == sensor_id]
        fig.add_trace(go.Scatter(
            x=sensor_hist['timestamp'],
            y=sensor_hist['value'],
            mode='lines',
            name=f"{sensor_id} (Normal)",
            line=dict(width=1)
        ))
        anomalies = sensor_hist[sensor_hist['is_anomaly'] == True]
        if not anomalies.empty:
            fig.add_trace(go.Scatter(
                x=anomalies['timestamp'],
                y=anomalies['value'],
                mode='markers',
                name=f"{sensor_id} (Anomaly)",
                marker=dict(color='red', size=8, symbol='x')
            ))
    fig.update_layout(height=500, title="Real-time Sensor Data with Detected Anomalies", xaxis_title="Time", yaxis_title="Value")
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    if st.session_state.alert_log:
        alert_df = pd.DataFrame(st.session_state.alert_log)
        def color_severity(val):
            color = 'red' if val == 'HIGH' else 'orange' if val == 'MEDIUM' else 'yellow'
            return f'color: {color}'
        display_df = alert_df[['timestamp', 'sensor_id', 'severity', 'message']].copy().sort_values(by='timestamp', ascending=False).head(50)
        alert_placeholder.dataframe(display_df.style.map(color_severity, subset=['severity']), use_container_width=True, hide_index=True)
