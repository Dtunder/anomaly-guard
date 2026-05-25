# Deployment Guide

This guide describes how to deploy the AnomalyGuard MVP to Streamlit Community Cloud.

## Streamlit Community Cloud

The easiest way to deploy this interactive dashboard is via Streamlit Community Cloud.

### Prerequisites
1. A GitHub account with the code pushed to a repository.
2. A Streamlit Community Cloud account (free).

### Deployment Steps
1. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click **New app**.
3. Select the repository, branch (e.g., `main` or `feat/mvp-implementation`), and set the main file path to `app.py`.
4. Click **Deploy!**

### Configuring Environment Variables
Once deployed, you need to configure the required environment variables:
1. In your Streamlit app dashboard, click on the **Settings** menu (three dots icon in the top right).
2. Go to **Secrets** (this acts as your `.env` file).
3. Add the following required environment variables:

```toml
MOCK_DATA = "true"
MOCK_LLM = "false"
USE_MOCK_MODEL = "false"
ALERT_THRESHOLD_HIGH = "0.8"
ALERT_THRESHOLD_MEDIUM = "0.6"
```

4. Save the secrets. The app will automatically restart and pick up the new variables.

## Alternative: Docker Deployment
If you prefer to deploy to your own infrastructure (e.g., a VPS or Railway), you can use the included `Dockerfile`.

```bash
docker build -t anomalyguard .
docker run -p 8501:8501 --env-file .env anomalyguard
```
