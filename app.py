from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xgboost as xgb
import pandas as pd

app = FastAPI(title="Fraud Detection API")

# Load model into memory at startup
model = xgb.XGBClassifier()
model.load_model("fraud_model.json")

# Define the expected JSON payload schema
class Transaction(BaseModel):
    amount: float
    is_international: int

@app.post("/predict")
def predict_fraud(transaction: Transaction):
    try:
        # Convert incoming JSON to the format XGBoost expects
        df = pd.DataFrame([{
            "amount": transaction.amount,
            "is_international": transaction.is_international
        }])
        
        # Extract the probability of class 1 (Fraud)
        probability = float(model.predict_proba(df)[0][1])
        
        return {
            "fraud_probability": probability,
            "risk_level": "High" if probability > 0.7 else "Low"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))