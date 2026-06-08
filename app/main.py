from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import numpy as np
import requests
from datetime import datetime

app = FastAPI(title="MLOps End-to-End Prediction Service")

# Point directly to the internal MLflow container network URL
MLFLOW_MODEL_URI = "http://mlflow-server:5000"
mlflow.set_tracking_uri(MLFLOW_MODEL_URI)

# Load the latest version of the registered model at startup
try:
    model = mlflow.pyfunc.load_model("models:/housing_model/latest")
    print("✅ Successfully loaded model from MLflow registry!")
except Exception as e:
    model = None
    print(f"❌ Warning: Could not load model from MLflow registry: {e}")

class HouseFeatures(BaseModel):
    square_feet: float

@app.get("/")
def health_check():
    return {"status": "Online", "model_loaded": model is not None}

@app.post("/predict")
def predict_price(data: HouseFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model artifact is not available yet.")
    
    # Format input array for sklearn inference
    input_array = np.array([[data.square_feet]])
    prediction = model.predict(input_array)
    
    return {
        "square_feet": data.square_feet,
        "estimated_price_thousands": float(prediction[0])
    }

def send_log_to_kibana(log_message: str, log_level: str = "INFO"):
    elasticsearch_url = "http://elasticsearch:9200/mlops-application-logs/_doc"
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": log_level,
        "message": log_message,
        "environment": "azure-production-vm"
    }
    try:
        requests.post(elasticsearch_url, json=payload, timeout=2)
    except Exception as e:
        print(f"Failed sending log to Elasticsearch: {e}")

# Example Usage inside your train.py or prediction endpoint:
send_log_to_kibana("Model training started successfully", "INFO")
send_log_to_kibana("Model version 2.8.1 registered to MLflow", "SUCCESS")
