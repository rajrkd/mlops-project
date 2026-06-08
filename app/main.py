from fastapi import FastAPI

app = FastAPI(title="MLOps Prediction API")

@app.get("/")
def read_root():
    return {"status": "Healthy", "message": "MLOps FastAPI Layer is Active!"}

@app.post("/predict")
def predict(data: dict):
    # This is where your model inference code will go later
    return {"prediction": "success", "input_received": data}
