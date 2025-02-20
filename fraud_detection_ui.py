import streamlit as st
import requests

st.title("Credit Card Fraud Detection")

st.write("Enter transaction details below to check if it's fraudulent.")

type_option = st.selectbox("Transaction Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN"])
amount = st.number_input("Transaction Amount", min_value=0.0, step=0.01)
oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0, step=0.01)
newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0, step=0.01)
oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0, step=0.01)
newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0, step=0.01)

if st.button("Check for Fraud"):
    data = {
        "type": type_option,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }
    
    response = requests.post("http://127.0.0.1:8000/predict", json=data)
    result = response.json()
    
    if "error" in result:
        st.error(result["error"])
    else:
        if result["isFraud"]:
            st.error("⚠️ This transaction is fraudulent!")
        else:
            st.success("✅ This transaction is NOT fraudulent.")