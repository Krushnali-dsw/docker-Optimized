from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Data Analysis API")

class DataPoint(BaseModel):
    x: float
    y: float

class PredictionRequest(BaseModel):
    data: list[DataPoint]
    predict_x: float

@app.get("/")
def read_root():
    return {"message": "FastAPI Data Analysis Server", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/analyze")
def analyze_data(request: PredictionRequest):
    """Perform simple linear regression using numpy and return prediction"""
    X = np.array([[point.x] for point in request.data])
    y = np.array([point.y for point in request.data])
    
    # Simple linear regression: y = mx + b
    # Using least squares: m = (n*Σxy - ΣxΣy) / (n*Σx² - (Σx)²)
    n = len(X)
    x_vals = X.flatten()
    sum_x = np.sum(x_vals)
    sum_y = np.sum(y)
    sum_xy = np.sum(x_vals * y)
    sum_x_squared = np.sum(x_vals ** 2)
    
    # Calculate slope (m) and intercept (b)
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x ** 2)
    b = (sum_y - m * sum_x) / n
    
    # Make prediction
    prediction = m * request.predict_x + b
    
    return {
        "prediction": float(prediction),
        "coefficient": float(m),
        "intercept": float(b),
        "data_points": len(request.data)
    }

@app.get("/stats")
def get_stats():
    """Return some basic statistics using numpy"""
    data = np.random.randn(1000)
    
    return {
        "mean": float(np.mean(data)),
        "std": float(np.std(data)),
        "min": float(np.min(data)),
        "max": float(np.max(data))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)