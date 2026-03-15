import streamlit as st
import requests

st.title("🛡️ FraudShield AI")

amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=100.0)
is_int = st.selectbox("International Transaction?", ["No", "Yes"])

# Convert "Yes/No" to 1/0 for the model
int_val = 1 if is_int == "Yes" else 0

if st.button("Run Fraud Analysis"):
    url = "https://fraud-api-353074659020.us-east1.run.app/predict"
    payload = {"amount": amount, "is_international": int_val}
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        prob = response.json()['fraud_probability']
        st.metric("Fraud Probability", f"{prob:.2%}")
    else:
        st.error("API Connection Failed")