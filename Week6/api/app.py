import sys
import os
import json
import joblib
import numpy as np

from fastapi import FastAPI


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from features.build_features import run_feature_pipeline

app = FastAPI()

model = joblib.load("models/best_model.pkl")

with open("features/feature_list.json") as f:
    feature_names = json.load(f)


@app.get("/")
def home():
    return {"message": "Model API is running"}

@app.post("/predict")
def predict(data: dict):


    input_data = np.array([list(data.values())])

    # prediction
    prediction = model.predict(input_data)[0]

    return {"prediction": int(prediction)}