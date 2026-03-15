# Real-Time Fraud Detection & MLOps Pipeline 🛡️

**Live API Endpoint:** [https://fraud-api-353074659020.us-east1.run.app/](https://fraud-api-353074659020.us-east1.run.app/)

---

### 📌 Project Overview
This project is a production-grade MLOps pipeline designed to detect fraudulent transactions in real-time. It features a containerized machine learning model, a high-performance API, and automated data drift monitoring.

### 🛠️ Technical Stack
* **Model:** XGBoost Classifier
* **API:** FastAPI (with Pydantic validation)
* **Monitoring:** Evidently AI (Statistical Drift Detection)
* **Cloud:** Google Cloud Run (Serverless)
* **DevOps:** Docker, GitHub, GCP Artifact Registry

### 📊 Data Drift Monitoring
To ensure long-term model reliability, this system uses **Evidently AI** to perform statistical tests (K-S test) on incoming data. It monitors for "Model Decay" by comparing live transaction features against the training baseline.

### 🚀 Usage (Test the Live API)
You can test the deployment directly from your terminal:
\`\`\`bash
curl -X POST "https://fraud-api-353074659020.us-east1.run.app/predict" \\
     -H "Content-Type: application/json" \\
     -d '{"amount": 5000.0, "is_international": 1}'
\`\`\`
