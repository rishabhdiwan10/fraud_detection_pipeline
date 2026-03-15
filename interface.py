cat << 'EOF' > interface.py
import streamlit as st
import requests

st.set_page_config(page_title="FraudShield AI", page_icon="🛡️")

st.title("🛡️ FraudShield: Real-Time Detection")
st.markdown("Enter transaction details below to get an instant fraud risk assessment.")

# User Inputs
amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=100.0)
is_int = st.selectbox("International Transaction?", ["No", "Yes"])

# Convert input to API format
int_val = 1 if is_int == "Yes" else 0

if st.button("Analyze Transaction"):
    # Hit your LIVE GCP URL
    url = "https://fraud-api-353074659020.us-east1.run.app/predict"
    payload = {"amount": amount, "is_international": int_val}
    
    with st.spinner('Querying Cloud AI...'):
        response = requests.post(url, json=payload)
        
    if response.status_status == 200:
        result = response.json()
        prob = result['fraud_probability']
        
        if prob > 0.5:
            st.error(f"⚠️ HIGH RISK: {prob:.2%} probability of fraud.")
        else:
            st.success(f"✅ LOW RISK: {prob:.2%} probability of fraud.")
    else:
        st.error("Error connecting to the Cloud API.")
EOF