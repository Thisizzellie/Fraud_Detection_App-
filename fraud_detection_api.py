from fastapi import FastAPI
import pickle
import pandas as pd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Load the trained model
with open("fraud_detection_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input data model
class TransactionInput(BaseModel):
    type: str
    amount: float
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float

# Transaction type mapping
type_mapping = {"PAYMENT": 0, "TRANSFER": 1, "CASH_OUT": 2, "DEBIT": 3, "CASH_IN": 4}

@app.post("/predict")
def predict_fraud(transaction: TransactionInput):
    transaction_type = type_mapping.get(transaction.type.upper(), -1)
    if transaction_type == -1:
        return {"error": "Invalid transaction type"}
    
    input_data = pd.DataFrame([[
        transaction_type,
        transaction.amount,
        transaction.oldbalanceOrg,
        transaction.newbalanceOrig,
        transaction.oldbalanceDest,
        transaction.newbalanceDest
    ]], columns=["type", "amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"])
    
    prediction = model.predict(input_data)[0]
    return {"isFraud": bool(prediction)}

# Run the API with uvicorn - uvicorn fraud_detection_api:app --reload
# Now the Streamlit app can send requests to the API to check for fraud - streamlit run fraud_detection_ui.py