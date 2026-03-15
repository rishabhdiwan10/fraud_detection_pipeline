import pandas as pd
import numpy as np
import xgboost as xgb
import mlflow
import mlflow.xgboost
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score

def generate_historical_data(n_samples=5000):
    """Generates synthetic training data matching our Kafka stream schema."""
    np.random.seed(42)
    amounts = np.random.uniform(5.0, 3000.0, n_samples)
    is_international = np.random.choice([0, 1], size=n_samples, p=[0.85, 0.15])
    
    # Define a simple fraud pattern for the model to learn:
    # High transaction amount + international location = high fraud probability
    fraud_prob = np.where((amounts > 1500) & (is_international == 1), 0.85, 0.05)
    labels = np.random.binomial(1, fraud_prob)
    
    return pd.DataFrame({'amount': amounts, 'is_international': is_international}), labels

print("Generating historical dataset...")
X, y = generate_historical_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Set up MLflow tracking
mlflow.set_experiment("Fraud_Detection_Experiment")

print("Training XGBoost model...")
with mlflow.start_run():
    # Define hyperparameters
    params = {
        "n_estimators": 100,
        "max_depth": 3,
        "learning_rate": 0.1,
        "objective": "binary:logistic"
    }
    
    # Initialize and train model
    model = xgb.XGBClassifier(**params)
    model.fit(X_train, y_train)
    
    # Evaluate model
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    precision = precision_score(y_test, preds)
    
    # Log to MLflow (This is the MLOps part of your resume)
    mlflow.log_params(params)
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("precision", precision)
    
    # Save the model artifact locally
    model_path = "fraud_model.json"
    model.save_model(model_path)
    
    print(f"Model trained successfully!")
    print(f"Accuracy: {acc:.2f} | Precision: {precision:.2f}")
    print(f"Model saved locally as: {model_path}")