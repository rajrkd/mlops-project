import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. Connect to our internal MLflow container
mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("Housing_Price_Prediction")

with mlflow.start_run():
    # 2. Dummy data: Area (sq ft) vs Price (in $1000s)
    X = np.array([[1000], [1500], [2000], [2500], [3000]])
    y = np.array([200, 300, 400, 500, 600])
    
    # 3. Train a basic model
    model = LinearRegression()
    model.fit(X, y)
    
    # 4. Log parameters and metrics
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_metric("coefficient", float(model.coef_[0]))
    
    # 5. Log the model into the registry with a fixed name
    mlflow.sklearn.log_model(
        sk_model=model, 
        artifact_path="model",
        registered_model_name="housing_model"
    )
    print("Successfully trained model and logged to MLflow!")
